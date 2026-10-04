from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import os
import re
import uuid
import time
import json
import logging
import bcrypt
import jwt

from collections import defaultdict
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Literal

from fastapi import (
    FastAPI,
    APIRouter,
    HTTPException,
    Depends,
    Request,
    Response,
    UploadFile,
    File,
)
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field, field_validator

import content as C


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s"
)

logger = logging.getLogger("dehaveda")


# ============================================================
# ENVIRONMENT / DATABASE / SECURITY
# ============================================================

MONGO_URL = os.environ.get(
    "MONGO_URL",
    "mongodb://localhost:27017"
)

DB_NAME = os.environ.get(
    "DB_NAME",
    "dehaveda"
)

JWT_SECRET = os.environ.get("JWT_SECRET", "").strip()

if not JWT_SECRET:
    JWT_SECRET = "dev-only-change-this-secret"

if (
    JWT_SECRET == "dev-only-change-this-secret"
    and os.environ.get("ENVIRONMENT", "development").lower() == "production"
):
    raise RuntimeError("JWT_SECRET must be set in production.")


client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

JWT_ALGORITHM = "HS256"

FREE_CHAT_LIMIT = 10


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Deha Veda Ecosystem API"
)


# ============================================================
# CORS
# ============================================================

CORS_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:3000,"
        "http://127.0.0.1:3000,"
        "https://deha-veda.onrender.com",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api = APIRouter(prefix="/api")

NO_ID = {"_id": 0}


# ============================================================
# HELPERS
# ============================================================

def now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.isoformat()


# ============================================================
# SECURITY HELPERS
# ============================================================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain.encode("utf-8"),
            hashed.encode("utf-8")
        )
    except ValueError:
        return False


def create_token(
    user_id: str,
    email: str,
    kind: str = "access"
) -> str:

    delta = (
        timedelta(days=7)
        if kind == "refresh"
        else timedelta(hours=12)
    )

    payload = {
        "sub": user_id,
        "email": email,
        "exp": now() + delta,
        "type": kind,
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )


def public_user(user: dict) -> dict:
    return {
        "id": user["id"],
        "name": user.get("name", ""),
        "email": user["email"],
        "role": user.get("role", "user"),
        "created_at": user.get("created_at"),
    }


def bearer_token(request: Request) -> Optional[str]:

    header = request.headers.get("Authorization", "")

    if header.startswith("Bearer "):
        return header[7:]

    return request.cookies.get("access_token")


async def get_current_user(request: Request) -> dict:

    token = bearer_token(request)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Session expired, please log in again"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )

    user = await db.users.find_one(
        {"id": payload["sub"]},
        NO_ID
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


async def get_optional_user(
    request: Request
) -> Optional[dict]:

    try:
        return await get_current_user(request)

    except HTTPException:
        return None


async def get_admin(
    user: dict = Depends(get_current_user)
) -> dict:

    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user


_rate_buckets: dict = defaultdict(list)


def rate_limit(
    key: str,
    limit: int,
    window_seconds: int
):

    bucket = _rate_buckets[key]

    cutoff = time.time() - window_seconds

    bucket[:] = [
        t for t in bucket
        if t > cutoff
    ]

    if len(bucket) >= limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests, please slow down."
        )

    bucket.append(time.time())


# ============================================================
# MODELS
# ============================================================

class RegisterIn(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=60
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )


class LoginIn(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=128
    )


class CalorieIn(BaseModel):

    age: int = Field(
        ge=10,
        le=100
    )

    sex: Literal["male", "female"]

    height_cm: float = Field(
        ge=90,
        le=250
    )

    weight_kg: float = Field(
        ge=25,
        le=300
    )

    activity: Literal[
        "sedentary",
        "light",
        "moderate",
        "active",
        "very_active"
    ]

    goal: Literal[
        "lose",
        "maintain",
        "gain"
    ]


class ChatIn(BaseModel):

    message: str = Field(
        min_length=1,
        max_length=1500
    )

    session_id: Optional[str] = None


class ContactIn(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=80
    )

    email: EmailStr

    subject: str = Field(
        min_length=3,
        max_length=120
    )

    message: str = Field(
        min_length=10,
        max_length=3000
    )


class FoodIn(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=80
    )

    category: str = Field(
        min_length=2,
        max_length=40
    )

    serving_size: str = "100 g"

    calories: float = Field(
        ge=0,
        le=1200
    )

    protein_g: float = Field(
        ge=0,
        le=200
    )

    carbs_g: float = Field(
        ge=0,
        le=200
    )

    fat_g: float = Field(
        ge=0,
        le=200
    )

    fiber_g: float = Field(
        ge=0,
        le=100
    )

    micronutrients: str = ""

    note: str = ""


class ContentIn(BaseModel):

    payload: dict


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
async def startup():

    await db.users.create_index(
        "email",
        unique=True
    )

    await db.users.create_index(
        "id",
        unique=True
    )

    await db.foods.create_index(
        [("name", 1)],
        unique=True
    )

    await db.foods.create_index(
        "category"
    )

    await db.chat_messages.create_index(
        [("session_id", 1), ("created_at", 1)]
    )

    await db.page_views.create_index(
        "path"
    )

    await db.health_reports.create_index(
        [("user_id", 1), ("created_at", -1)]
    )

    if await db.foods.count_documents({}) == 0:

        await db.foods.insert_many(
            [
                {
                    **f,
                    "id": str(uuid.uuid4())
                }
                for f in C.FOODS
            ]
        )

    admin_email = os.environ.get(
        "ADMIN_EMAIL",
        "admin@example.com"
    ).lower()

    admin_password = os.environ.get(
        "ADMIN_PASSWORD",
        "adminpassword123"
    )

    existing = await db.users.find_one(
        {"email": admin_email}
    )

    if existing is None:

        await db.users.insert_one(
            {
                "id": str(uuid.uuid4()),
                "name": "Deha Veda Admin",
                "email": admin_email,
                "password_hash": hash_password(
                    admin_password
                ),
                "role": "admin",
                "created_at": iso(now()),
            }
        )

        logger.info(
            "Seeded admin account %s",
            admin_email
        )

    elif not verify_password(
        admin_password,
        existing["password_hash"]
    ):

        await db.users.update_one(
            {"email": admin_email},
            {
                "$set": {
                    "password_hash": hash_password(
                        admin_password
                    )
                }
            }
        )


# ============================================================
# SHUTDOWN
# ============================================================

@app.on_event("shutdown")
async def shutdown():

    client.close()


# ============================================================
# AUTH
# ============================================================

def set_auth_cookies(
    response: Response,
    access: str,
    refresh: str
):

    cookie_secure = (
        os.environ.get(
            "COOKIE_SECURE",
            "false"
        ).strip().lower() == "true"
    )

    cookie_samesite = (
        "none"
        if cookie_secure
        else "lax"
    )

    response.set_cookie(
        "access_token",
        access,
        httponly=True,
        secure=cookie_secure,
        samesite=cookie_samesite,
        max_age=43200,
        path="/",
    )

    response.set_cookie(
        "refresh_token",
        refresh,
        httponly=True,
        secure=cookie_secure,
        samesite=cookie_samesite,
        max_age=604800,
        path="/",
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "deha-veda-backend"
    }


@api.get("/")
async def root():
    return {
        "service": "Deha Veda Ecosystem API",
        "status": "ok"
    }


@api.post("/auth/register")
async def register(
    body: RegisterIn,
    request: Request,
    response: Response
):

    rate_limit(
        f"reg:{request.client.host}",
        60,
        3600
    )

    email = body.email.lower().strip()

    if await db.users.find_one({"email": email}):

        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists"
        )

    user = {
        "id": str(uuid.uuid4()),
        "name": body.name.strip(),
        "email": email,
        "password_hash": hash_password(body.password),
        "role": "user",
        "created_at": iso(now()),
    }

    await db.users.insert_one(dict(user))

    access = create_token(
        user["id"],
        email
    )

    set_auth_cookies(
        response,
        access,
        create_token(
            user["id"],
            email,
            "refresh"
        )
    )

    return {
        "token": access,
        "user": public_user(user)
    }


@api.post("/auth/login")
async def login(
    body: LoginIn,
    request: Request,
    response: Response
):

    email = body.email.lower().strip()

    ident = email

    attempt = await db.login_attempts.find_one(
        {"identifier": ident},
        NO_ID
    )

    if attempt and attempt.get("count", 0) >= 5:

        locked_until = datetime.fromisoformat(
            attempt["locked_until"]
        )

        if locked_until > now():

            raise HTTPException(
                status_code=429,
                detail="Too many failed attempts. Try again in a few minutes."
            )

    user = await db.users.find_one(
        {"email": email},
        NO_ID
    )

    if (
        not user
        or not verify_password(
            body.password,
            user["password_hash"]
        )
    ):

        await db.login_attempts.update_one(
            {"identifier": ident},
            {
                "$inc": {
                    "count": 1
                },
                "$set": {
                    "locked_until": iso(
                        now() + timedelta(minutes=15)
                    )
                }
            },
            upsert=True,
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    await db.login_attempts.delete_one(
        {"identifier": ident}
    )

    access = create_token(
        user["id"],
        email
    )

    set_auth_cookies(
        response,
        access,
        create_token(
            user["id"],
            email,
            "refresh"
        )
    )

    return {
        "token": access,
        "user": public_user(user)
    }


@api.get("/auth/me")
async def me(
    user: dict = Depends(get_current_user)
):

    return public_user(user)


@api.post("/auth/logout")
async def logout(
    response: Response
):

    response.delete_cookie(
        "access_token",
        path="/"
    )

    response.delete_cookie(
        "refresh_token",
        path="/"
    )

    return {
        "ok": True
    }


# ============================================================
# COMMUNITY STATS
# ============================================================

@api.get("/stats/community")
async def community_stats():

    total = await db.users.count_documents(
        {
            "role": {
                "$ne": "admin"
            }
        }
    )

    return {
        "community_members": total,
        "foods_catalogued": await db.foods.count_documents({})
    }


# ============================================================
# AHARA
# ============================================================

@api.get("/foods/categories")
async def food_categories():

    return {
        "categories": C.FOOD_CATEGORIES
    }


@api.get("/foods")
async def list_foods(
    q: str = "",
    category: str = ""
):

    query: dict = {}

    if q.strip():

        query["name"] = {
            "$regex": re.escape(q.strip()),
            "$options": "i"
        }

    if (
        category.strip()
        and category != "All"
    ):

        query["category"] = category.strip()

    # Exclude legacy premium field
    projection = {
        **NO_ID,
        "premium": 0
    }

    docs = await db.foods.find(
        query,
        projection
    ).sort(
        "name",
        1
    ).to_list(500)

    items = [
        {
            **d,
            "locked": False
        }
        for d in docs
    ]

    return {
        "items": items,
        "total": len(items),
        "locked_count": 0,
        "is_premium": True,
    }


# ============================================================
# CALORIE TOOL
# ============================================================

@api.post("/tools/calorie")
async def calorie(
    body: CalorieIn
):

    if body.sex == "male":

        bmr = (
            10 * body.weight_kg
            + 6.25 * body.height_cm
            - 5 * body.age
            + 5
        )

    else:

        bmr = (
            10 * body.weight_kg
            + 6.25 * body.height_cm
            - 5 * body.age
            - 161
        )

    factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }

    maintenance = (
        bmr * factors[body.activity]
    )

    if body.goal == "lose":

        low = maintenance - 500
        high = maintenance - 250
        label = "Gradual fat loss"

    elif body.goal == "gain":

        low = maintenance + 250
        high = maintenance + 500
        label = "Gradual weight gain"

    else:

        low = maintenance - 100
        high = maintenance + 100
        label = "Weight maintenance"

    bmi = (
        body.weight_kg
        / ((body.height_cm / 100) ** 2)
    )

    return {
        "bmr": round(bmr),
        "maintenance": round(maintenance),
        "goal_label": label,
        "goal_range": [
            round(low),
            round(high)
        ],
        "bmi": round(bmi, 1),
        "protein_g_range": [
            round(body.weight_kg * 1.2),
            round(body.weight_kg * 1.6)
        ],
        "formula": (
            "Mifflin-St Jeor equation with standard "
            "activity multipliers"
        ),
        "disclaimer": (
            "These figures are population-level estimates, "
            "not medical or dietary advice. Individual needs "
            "vary. Consult a qualified professional before "
            "making changes."
        ),
    }


# ============================================================
# JALA
# ============================================================

@api.get("/jala")
async def jala():

    water_types = [
        {
            k: v
            for k, v in wt.items()
            if k != "premium"
        }
        | {
            "locked": False
        }
        for wt in C.WATER_TYPES
    ]

    parameters = [
        {
            k: v
            for k, v in wp.items()
            if k != "premium"
        }
        | {
            "locked": False
        }
        for wp in C.WATER_PARAMETERS
    ]

    return {
        "water_types": water_types,
        "journey": C.WATER_JOURNEY,
        "parameters": parameters,
        "contamination": C.WATER_CONTAMINATION,
        "gallery": C.WATER_GALLERY,
        "is_premium": True,
        "sources": (
            "WHO Guidelines for Drinking-water Quality "
            "(4th ed.) and BIS IS 10500:2012."
        ),
    }


# ============================================================
# MANAS
# ============================================================

@api.get("/manas")
async def manas():

    topics = [
        {
            k: v
            for k, v in t.items()
            if k != "premium"
        }
        | {
            "locked": False
        }
        for t in C.MANAS_TOPICS
    ]

    return {
        "topics": topics,
        "brain_regions": C.BRAIN_REGIONS,
        "peaceful_mind": C.PEACEFUL_MIND,
        "is_premium": True,
        "note": (
            "This is a simplified educational brain model, "
            "not an anatomically precise medical illustration. "
            "The 'mind' is described as a set of functions, "
            "not a physical structure with a location."
        ),
    }


# ============================================================
# AI ASSISTANT
# ============================================================

SYSTEM_PROMPT = (
    "You are the Deha Veda AI Assistant for the DEHA VEDA "
    "ECOSYSTEM platform, which teaches three pillars: "
    "AHARA (food and nutrition), JALA (water and water quality), "
    "and MANAS (mind and brain).\n"
    "Rules you must always follow:\n"
    "1. Answer only questions related to these three pillars "
    "or to using this website. If asked something unrelated, "
    "politely redirect to the three pillars.\n"
    "2. You are NOT a doctor, dietitian or therapist and must "
    "never present yourself as one. Never diagnose, never "
    "prescribe, never claim any food, water, or mental exercise "
    "cures a disease.\n"
    "3. Give general educational information, give approximate "
    "numbers with the serving size they refer to, and say when "
    "values vary.\n"
    "4. For any personal medical, nutritional or mental-health "
    "concern, recommend consulting a qualified professional.\n"
    "5. Keep answers concise: 2 to 5 short paragraphs or a "
    "compact list. Plain text, no markdown headings."
)


@api.get("/chat/history")
async def chat_history(
    session_id: str,
    user: Optional[dict] = Depends(
        get_optional_user
    )
):

    query = {
        "session_id": session_id
    }

    if user:

        query["user_id"] = user["id"]

    docs = await db.chat_messages.find(
        query,
        NO_ID
    ).sort(
        "created_at",
        1
    ).to_list(100)

    return {
        "messages": docs
    }


@api.post("/chat")
async def chat(
    body: ChatIn,
    request: Request,
    user: Optional[dict] = Depends(
        get_optional_user
    )
):

    session_id = (
        body.session_id
        or str(uuid.uuid4())
    )

    ip = request.client.host

    rate_limit(
        f"chat:{ip}",
        30,
        300
    )

    if user:

        since = iso(
            now() - timedelta(days=1)
        )

        used = await db.chat_messages.count_documents(
            {
                "user_id": user["id"],
                "role": "user",
                "created_at": {
                    "$gte": since
                },
            }
        )

        if used >= FREE_CHAT_LIMIT:

            raise HTTPException(
                status_code=403,
                detail=(
                    f"Daily message limit reached "
                    f"({FREE_CHAT_LIMIT}). Please try again tomorrow."
                ),
            )

    api_key = os.environ.get(
        "EMERGENT_LLM_KEY"
    )

    if not api_key:

        raise HTTPException(
            status_code=503,
            detail=(
                "AI assistant is not configured on the server."
            )
        )

    prior = await db.chat_messages.find(
        {
            "session_id": session_id
        },
        NO_ID
    ).sort(
        "created_at",
        1
    ).to_list(20)

    await db.chat_messages.insert_one(
        {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "user_id": (
                user["id"]
                if user
                else None
            ),
            "role": "user",
            "text": body.message,
            "created_at": iso(now()),
        }
    )

    from emergentintegrations.llm.chat import (
        LlmChat,
        UserMessage,
        TextDelta,
        StreamDone,
    )

    history_text = "\n".join(
        f"{m['role']}: {m['text']}"
        for m in prior[-8:]
    )

    chat_client = (
        LlmChat(
            api_key=api_key,
            session_id=session_id,
            system_message=(
                SYSTEM_PROMPT
                + (
                    f"\n\nRecent conversation:\n{history_text}"
                    if history_text
                    else ""
                )
            ),
        )
        .with_model(
            "openai",
            "gpt-5.5"
        )
    )

    async def generator():

        collected = []

        try:

            async for event in chat_client.stream_message(
                UserMessage(
                    text=body.message
                )
            ):

                if isinstance(
                    event,
                    TextDelta
                ):

                    collected.append(
                        event.content
                    )

                    yield (
                        f"data: "
                        f"{json.dumps({'delta': event.content})}"
                        "\n\n"
                    )

                elif isinstance(
                    event,
                    StreamDone
                ):

                    break

        except Exception as exc:

            logger.exception(
                "AI stream failed"
            )

            yield (
                f"data: "
                f"{json.dumps({'error': 'The assistant could not respond right now.'})}"
                "\n\n"
            )

            _ = exc

        answer = "".join(collected)

        if answer:

            await db.chat_messages.insert_one(
                {
                    "id": str(uuid.uuid4()),
                    "session_id": session_id,
                    "user_id": (
                        user["id"]
                        if user
                        else None
                    ),
                    "role": "assistant",
                    "text": answer,
                    "created_at": iso(now()),
                }
            )

        yield (
            f"data: "
            f"{json.dumps({'done': True, 'session_id': session_id})}"
            "\n\n"
        )

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


# ============================================================
# HEALTH REPORTS
# ============================================================

HEALTH_PROMPT = (
    "You are a careful medical-document parser. Read the attached "
    "lab or health report and return ONLY valid JSON, no prose, "
    "no markdown fences, matching exactly this shape:\n"
    '{"report_title": str, "report_date": str, "lab_name": str, '
    '"patient_age": str, "patient_sex": str, "panels": [str], '
    '"tests": [{"name": str, "value": str, "unit": str, '
    '"reference_range": str, "status": "low"|"normal"|"high"|"unknown", '
    '"plain_english": str}], "key_findings": [str], '
    '"lifestyle_notes": [str], "questions_for_doctor": [str], '
    '"summary": str}\n'
    'Rules: use "" for anything not printed in the report; '
    "never invent values or reference ranges; derive status only "
    "by comparing the printed value with the printed reference "
    'range, otherwise "unknown"; plain_english explains what the '
    "test measures in one short sentence; lifestyle_notes are "
    "general educational points only. You are NOT a doctor: do "
    "not diagnose, do not name diseases as conclusions, do not "
    "suggest medication or dosage. summary is 2-3 sentences of "
    "neutral description ending with a reminder to discuss results "
    "with a qualified clinician."
)


ALLOWED_REPORT_TYPES = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "text/plain": ".txt",
}


def _extract_json(raw: str) -> dict:

    text = raw.strip()

    if text.startswith("```"):

        text = re.sub(
            r"^```[a-zA-Z]*\n?",
            "",
            text
        )

        text = re.sub(
            r"```$",
            "",
            text
        ).strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:

        raise ValueError(
            "No JSON object in model output"
        )

    return json.loads(
        text[start:end + 1]
    )


HEALTH_DISCLAIMER = (
    "This is an automated reading of your own document for "
    "educational understanding only. It is not a diagnosis, "
    "not a second opinion and not medical advice. Values can "
    "be misread from poor scans. Always discuss your results "
    "with a qualified clinician."
)


@api.post("/health/reports")
async def upload_health_report(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
):

    rate_limit(
        f"health:{user['id']}",
        12,
        3600
    )

    upload = file

    if upload.content_type not in ALLOWED_REPORT_TYPES:

        raise HTTPException(
            status_code=400,
            detail=(
                "Upload a PDF, JPG, PNG, WEBP or TXT "
                "file of your report"
            )
        )

    blob = await upload.read()

    if len(blob) > 10 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="File is larger than 10 MB"
        )

    if not blob:

        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty"
        )

    api_key = os.environ.get(
        "EMERGENT_LLM_KEY"
    )

    if not api_key:

        raise HTTPException(
            status_code=503,
            detail=(
                "Report analysis is not configured "
                "on the server."
            )
        )

    import tempfile

    suffix = ALLOWED_REPORT_TYPES[
        upload.content_type
    ]

    tmp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    tmp.write(blob)
    tmp.close()

    try:

        from emergentintegrations.llm.chat import (
            LlmChat,
            UserMessage,
            FileContentWithMimeType,
            TextDelta,
            StreamDone,
        )

        chat = (
            LlmChat(
                api_key=api_key,
                session_id=f"health-{uuid.uuid4()}",
                system_message=HEALTH_PROMPT
            )
            .with_model(
                "gemini",
                "gemini-3.1-pro-preview"
            )
        )

        attachment = FileContentWithMimeType(
            file_path=tmp.name,
            mime_type=upload.content_type
        )

        chunks = []

        async for ev in chat.stream_message(
            UserMessage(
                text=(
                    "Parse this report into the JSON schema."
                ),
                file_contents=[
                    attachment
                ]
            )
        ):

            if isinstance(
                ev,
                TextDelta
            ):

                chunks.append(
                    ev.content
                )

            elif isinstance(
                ev,
                StreamDone
            ):

                break

        parsed = _extract_json(
            "".join(chunks)
        )

    except HTTPException:
        raise

    except json.JSONDecodeError:

        logger.exception(
            "Health report JSON parse failed"
        )

        raise HTTPException(
            status_code=422,
            detail=(
                "The report could not be read reliably. "
                "Try a clearer scan or a PDF."
            )
        )

    except Exception as exc:

        logger.exception(
            "Health report analysis failed"
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "The report could not be analysed right now. "
                "Please try again."
            )
        ) from exc

    finally:

        os.unlink(tmp.name)

    tests = parsed.get("tests") or []

    doc = {
        "id": str(uuid.uuid4()),
        "user_id": user["id"],
        "file_name": (
            upload.filename
            or "report"
        ),
        "mime_type": upload.content_type,
        "report_title": (
            parsed.get("report_title")
            or "Health report"
        ),
        "report_date": (
            parsed.get("report_date")
            or ""
        ),
        "lab_name": (
            parsed.get("lab_name")
            or ""
        ),
        "patient_age": (
            parsed.get("patient_age")
            or ""
        ),
        "patient_sex": (
            parsed.get("patient_sex")
            or ""
        ),
        "panels": (
            parsed.get("panels")
            or []
        ),
        "tests": tests,
        "key_findings": (
            parsed.get("key_findings")
            or []
        ),
        "lifestyle_notes": (
            parsed.get("lifestyle_notes")
            or []
        ),
        "questions_for_doctor": (
            parsed.get("questions_for_doctor")
            or []
        ),
        "summary": (
            parsed.get("summary")
            or ""
        ),
        "counts": {
            "total": len(tests),
            "normal": sum(
                1
                for t in tests
                if t.get("status") == "normal"
            ),
            "high": sum(
                1
                for t in tests
                if t.get("status") == "high"
            ),
            "low": sum(
                1
                for t in tests
                if t.get("status") == "low"
            ),
            "unknown": sum(
                1
                for t in tests
                if t.get("status")
                not in (
                    "normal",
                    "high",
                    "low"
                )
            ),
        },
        "created_at": iso(now()),
    }

    await db.health_reports.insert_one(
        dict(doc)
    )

    return {
        "report": doc,
        "disclaimer": HEALTH_DISCLAIMER
    }


@api.get("/health/reports")
async def list_health_reports(
    user: dict = Depends(get_current_user)
):

    docs = await db.health_reports.find(
        {
            "user_id": user["id"]
        },
        NO_ID
    ).sort(
        "created_at",
        -1
    ).to_list(50)

    return {
        "reports": docs,
        "disclaimer": HEALTH_DISCLAIMER
    }


@api.delete("/health/reports/{report_id}")
async def delete_health_report(
    report_id: str,
    user: dict = Depends(get_current_user)
):

    res = await db.health_reports.delete_one(
        {
            "id": report_id,
            "user_id": user["id"]
        }
    )

    if res.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return {
        "deleted": True
    }


@api.get("/health/profile")
async def health_profile(
    user: dict = Depends(get_current_user)
):

    docs = await db.health_reports.find(
        {
            "user_id": user["id"]
        },
        NO_ID
    ).sort(
        "created_at",
        1
    ).to_list(50)

    totals = {
        "total": 0,
        "normal": 0,
        "high": 0,
        "low": 0,
        "unknown": 0
    }

    attention = []
    timeline = []
    trends = {}

    for d in docs:

        for k in totals:

            totals[k] += d.get(
                "counts",
                {}
            ).get(
                k,
                0
            )

        timeline.append(
            {
                "date": (
                    d.get("report_date")
                    or d["created_at"]
                )[:10],
                "title": d.get(
                    "report_title",
                    ""
                ),
                "normal": d.get(
                    "counts",
                    {}
                ).get(
                    "normal",
                    0
                ),
                "flagged": (
                    d.get(
                        "counts",
                        {}
                    ).get(
                        "high",
                        0
                    )
                    +
                    d.get(
                        "counts",
                        {}
                    ).get(
                        "low",
                        0
                    )
                ),
            }
        )

        for t in d.get(
            "tests",
            []
        ):

            if t.get("status") in (
                "high",
                "low"
            ):

                attention.append(
                    {
                        "name": t.get(
                            "name",
                            ""
                        ),
                        "value": t.get(
                            "value",
                            ""
                        ),
                        "unit": t.get(
                            "unit",
                            ""
                        ),
                        "reference_range": t.get(
                            "reference_range",
                            ""
                        ),
                        "status": t.get(
                            "status"
                        ),
                        "plain_english": t.get(
                            "plain_english",
                            ""
                        ),
                        "date": (
                            d.get(
                                "report_date"
                            )
                            or d["created_at"]
                        )[:10],
                    }
                )

            name = (
                t.get("name")
                or ""
            ).strip()

            if name:

                trends.setdefault(
                    name,
                    []
                ).append(
                    {
                        "date": (
                            d.get(
                                "report_date"
                            )
                            or d["created_at"]
                        )[:10],
                        "value": t.get(
                            "value",
                            ""
                        ),
                        "unit": t.get(
                            "unit",
                            ""
                        ),
                        "status": t.get(
                            "status"
                        ),
                    }
                )

    latest = (
        docs[-1]
        if docs
        else None
    )

    return {
        "reports_count": len(docs),
        "totals": totals,
        "attention": attention[-12:],
        "timeline": timeline,
        "trends": {
            k: v
            for k, v in trends.items()
            if len(v) > 1
        },
        "latest_summary": (
            latest.get(
                "summary",
                ""
            )
            if latest
            else ""
        ),
        "lifestyle_notes": (
            latest.get(
                "lifestyle_notes",
                []
            )
            if latest
            else []
        ),
        "questions_for_doctor": (
            latest.get(
                "questions_for_doctor",
                []
            )
            if latest
            else []
        ),
        "disclaimer": HEALTH_DISCLAIMER,
    }


# ============================================================
# CONTACT
# ============================================================

@api.post("/contact")
async def contact(
    body: ContactIn,
    request: Request
):

    rate_limit(
        f"contact:{request.client.host}",
        5,
        3600
    )

    doc = {
        "id": str(uuid.uuid4()),
        "name": body.name.strip(),
        "email": body.email.lower(),
        "subject": body.subject.strip(),
        "message": body.message.strip(),
        "status": "new",
        "created_at": iso(now()),
    }

    await db.contact_messages.insert_one(
        dict(doc)
    )

    return {
        "received": True,
        "message": (
            "Thank you. Your message has been recorded "
            "and we will reply by email."
        )
    }


# ============================================================
# PAGE TRACKING
# ============================================================

class TrackIn(BaseModel):

    path: str = Field(
        min_length=1,
        max_length=120
    )


@api.post("/track")
async def track(
    body: TrackIn
):

    await db.page_views.update_one(
        {
            "path": body.path
        },
        {
            "$inc": {
                "views": 1
            }
        },
        upsert=True,
    )

    return {
        "ok": True
    }


# ============================================================
# ADMIN
# ============================================================

@api.get("/admin/stats")
async def admin_stats(
    admin: dict = Depends(get_admin)
):

    week_ago = iso(
        now() - timedelta(days=7)
    )

    total_users = await db.users.count_documents(
        {
            "role": {
                "$ne": "admin"
            }
        }
    )

    new_week = await db.users.count_documents(
        {
            "created_at": {
                "$gte": week_ago
            },
            "role": {
                "$ne": "admin"
            }
        }
    )

    registrations = []

    for i in range(
        6,
        -1,
        -1
    ):

        day = (
            now()
            - timedelta(days=i)
        ).date().isoformat()

        count = await db.users.count_documents(
            {
                "role": {
                    "$ne": "admin"
                },
                "created_at": {
                    "$gte": day,
                    "$lt": (
                        day
                        + "T23:59:59.999999+00:00"
                    ),
                },
            }
        )

        registrations.append(
            {
                "day": day[5:],
                "users": count
            }
        )

    pages = await db.page_views.find(
        {},
        NO_ID
    ).sort(
        "views",
        -1
    ).to_list(12)

    ai_messages = await db.chat_messages.count_documents(
        {
            "role": "user"
        }
    )

    return {
        "total_users": total_users,
        "new_registrations_7d": new_week,
        "contact_messages": (
            await db.contact_messages.count_documents({})
        ),
        "ai_messages": ai_messages,
        "registrations_7d": registrations,
        "popular_pages": pages,
    }


@api.get("/admin/users")
async def admin_users(
    admin: dict = Depends(get_admin)
):

    docs = await db.users.find(
        {},
        NO_ID
    ).sort(
        "created_at",
        -1
    ).to_list(500)

    return {
        "users": [
            public_user(d)
            for d in docs
        ]
    }


@api.post("/admin/foods")
async def create_food(
    body: FoodIn,
    admin: dict = Depends(get_admin)
):

    if await db.foods.find_one(
        {
            "name": body.name
        }
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "A food with this name already exists"
            )
        )

    doc = {
        **body.model_dump(),
        "id": str(uuid.uuid4()),
        "source": "Admin entry"
    }

    await db.foods.insert_one(
        dict(doc)
    )

    return doc


@api.put("/admin/foods/{food_id}")
async def update_food(
    food_id: str,
    body: FoodIn,
    admin: dict = Depends(get_admin)
):

    result = await db.foods.update_one(
        {
            "id": food_id
        },
        {
            "$set": body.model_dump()
        }
    )

    if result.matched_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    return await db.foods.find_one(
        {
            "id": food_id
        },
        NO_ID
    )


@api.delete("/admin/foods/{food_id}")
async def delete_food(
    food_id: str,
    admin: dict = Depends(get_admin)
):

    result = await db.foods.delete_one(
        {
            "id": food_id
        }
    )

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    return {
        "deleted": True
    }


@api.get("/admin/contact")
async def admin_contact(
    admin: dict = Depends(get_admin)
):

    docs = await db.contact_messages.find(
        {},
        NO_ID
    ).sort(
        "created_at",
        -1
    ).to_list(200)

    return {
        "messages": docs
    }


@api.get("/admin/content/{key}")
async def get_editable_content(
    key: str,
    admin: dict = Depends(get_admin)
):

    doc = await db.editable_content.find_one(
        {
            "key": key
        },
        NO_ID
    )

    return doc or {
        "key": key,
        "payload": {}
    }


@api.put("/admin/content/{key}")
async def put_editable_content(
    key: str,
    body: ContentIn,
    admin: dict = Depends(get_admin)
):

    await db.editable_content.update_one(
        {
            "key": key
        },
        {
            "$set": {
                "payload": body.payload,
                "updated_at": iso(now())
            }
        },
        upsert=True,
    )

    return {
        "key": key,
        "payload": body.payload
    }


# ============================================================
# REGISTER ALL API ROUTES
# ============================================================

app.include_router(api)