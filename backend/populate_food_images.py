import asyncio
import os
import re
import time
from pathlib import Path
from urllib.parse import quote

import aiohttp
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


# ============================================================
# DEHA VEDA — FREE REAL FOOD PHOTO IMPORTER
# ============================================================
#
# Source:
#   Wikimedia Commons
#
# Cost:
#   ₹0
#
# What this script does:
#   1. Reads the exact 64 foods from MongoDB
#   2. Searches Wikimedia Commons
#   3. Applies STRICT matching
#   4. Rejects questionable matches
#   5. Downloads real photographs locally
#   6. Stores image_url + attribution metadata in MongoDB
#
# It does NOT:
#   - use OpenAI
#   - use AI image generation
#   - use Openverse
#   - use generic image-search results
#   - modify server.py
#   - modify Ahara.jsx
#   - require manual mapping
#
# ============================================================


# ------------------------------------------------------------
# LOAD ENV
# ------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "dehaveda")


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

PROJECT_ROOT = ROOT_DIR.parent

IMAGE_DIR = (
    PROJECT_ROOT
    / "frontend"
    / "public"
    / "images"
    / "food"
    / "items"
)

IMAGE_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# WIKIMEDIA COMMONS
# ------------------------------------------------------------

COMMONS_API = "https://commons.wikimedia.org/w/api.php"

USER_AGENT = (
    "DehaVedaFoodImporter/1.0 "
    "(educational project; respectful API usage)"
)


# ------------------------------------------------------------
# SEARCH ALIASES
# ------------------------------------------------------------
#
# These are NOT image URLs.
#
# They simply tell the importer that some foods have common
# alternative names.
#
# The script still applies strict matching.
# ------------------------------------------------------------

ALIASES = {
    "Bottle Gourd": [
        "bottle gourd",
        "lauki",
        "calabash",
    ],

    "Okra (Bhindi)": [
        "okra",
        "bhindi",
        "lady finger",
    ],

    "Finger Millet (Ragi)": [
        "finger millet",
        "ragi",
    ],

    "Pearl Millet (Bajra)": [
        "pearl millet",
        "bajra",
    ],

    "Pigeon Pea (Toor Dal)": [
        "pigeon pea",
        "toor dal",
        "toor",
        "arhar dal",
    ],

    "Green Gram (Moong)": [
        "green gram",
        "moong",
        "mung bean",
        "mung",
    ],

    "Red Lentils (Masoor Dal)": [
        "red lentils",
        "masoor dal",
        "masoor",
    ],

    "Kidney Beans (Rajma)": [
        "kidney beans",
        "rajma",
    ],

    "Chickpeas (Chana)": [
        "chickpeas",
        "chana",
        "garbanzo beans",
    ],

    "Cow Milk (Whole)": [
        "cow milk",
        "whole milk",
        "milk",
    ],

    "Curd / Yogurt (Plain)": [
        "curd",
        "yogurt",
        "yoghurt",
    ],

    "Buttermilk (Chaas)": [
        "buttermilk",
        "chaas",
    ],

    "Makhana (Fox Nut)": [
        "makhana",
        "fox nut",
        "foxnuts",
        "lotus seeds",
    ],

    "Roasted Chana": [
        "roasted chana",
        "roasted chickpeas",
        "roasted gram",
    ],

    "Rohu Fish": [
        "rohu",
        "rohu fish",
        "labeo rohita",
    ],

    "Masala Chai (with milk & sugar)": [
        "masala chai",
        "masala tea",
    ],

    "Lemon Water (no sugar)": [
        "lemon water",
        "lemon juice water",
    ],

    "Green Tea (unsweetened)": [
        "green tea",
    ],

    "Coconut Water": [
        "coconut water",
    ],

    "Fruit Chaat": [
        "fruit chaat",
        "fruit chat",
    ],

    "Sprouts Salad": [
        "sprouts salad",
        "sprouted salad",
    ],

    "Egg (Whole, boiled)": [
        "boiled egg",
        "hard boiled egg",
        "hard-boiled egg",
    ],

    "Chicken Breast (cooked)": [
        "chicken breast",
        "cooked chicken breast",
    ],

    "Soybean (boiled)": [
        "boiled soybean",
        "boiled soybeans",
        "soybean",
        "soybeans",
    ],

    "Sweet Potato": [
        "sweet potato",
    ],

    "Whole Wheat Flour": [
        "whole wheat flour",
        "wholemeal flour",
        "atta",
    ],
}


# ------------------------------------------------------------
# WORD NORMALIZATION
# ------------------------------------------------------------

STOP_WORDS = {
    "food",
    "foods",
    "photo",
    "photograph",
    "photography",
    "image",
    "images",
    "dish",
    "meal",
    "plate",
    "fresh",
    "freshly",
    "cooked",
    "cooking",
    "recipe",
    "recipes",
    "healthy",
    "delicious",
}


def normalize(text: str) -> str:
    text = text.lower()

    text = text.replace("&", " and ")
    text = re.sub(r"[\(\)\[\]\{\},:;/_\-]", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    words = text.split()

    words = [
        w for w in words
        if w not in STOP_WORDS
    ]

    return " ".join(words)


def tokens(text: str):
    return set(normalize(text).split())


# ------------------------------------------------------------
# SLUG
# ------------------------------------------------------------

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


# ------------------------------------------------------------
# SEARCH TERMS
# ------------------------------------------------------------

def get_search_terms(food_name: str):
    terms = []

    aliases = ALIASES.get(food_name)

    if aliases:
        terms.extend(aliases)

    # Main name without parenthetical explanation
    base = re.sub(r"\([^)]*\)", "", food_name).strip()

    if base:
        terms.append(base)

    terms.append(food_name)

    # Preserve order while removing duplicates
    result = []

    for term in terms:
        term = term.strip()

        if term and term.lower() not in {
            x.lower() for x in result
        }:
            result.append(term)

    return result


# ------------------------------------------------------------
# SEARCH SCORE
# ------------------------------------------------------------

def score_result(food_name: str, title: str):
    """
    Strict scoring.

    We deliberately prefer false negatives over false positives.
    """

    title_norm = normalize(title)
    title_tokens = tokens(title)

    aliases = ALIASES.get(food_name, [])

    expected_phrases = []

    base = re.sub(r"\([^)]*\)", "", food_name).strip()

    if base:
        expected_phrases.append(normalize(base))

    for alias in aliases:
        expected_phrases.append(normalize(alias))

    expected_phrases = [
        p for p in expected_phrases if p
    ]

    best_score = 0

    # --------------------------------------------------------
    # EXACT PHRASE MATCH
    # --------------------------------------------------------

    for phrase in expected_phrases:

        if phrase == title_norm:
            best_score = max(best_score, 1000)

        elif f" {phrase} " in f" {title_norm} ":
            best_score = max(best_score, 800)

    # --------------------------------------------------------
    # TOKEN MATCH
    # --------------------------------------------------------

    expected_tokens = set()

    for phrase in expected_phrases:
        expected_tokens.update(phrase.split())

    if expected_tokens:

        matched = expected_tokens.intersection(title_tokens)

        ratio = len(matched) / len(expected_tokens)

        if ratio == 1:
            best_score = max(best_score, 700)

        elif ratio >= 0.75:
            best_score = max(best_score, 500)

    # --------------------------------------------------------
    # PENALTIES FOR OBVIOUSLY WRONG RESULTS
    # --------------------------------------------------------

    bad_words = {
        "juice",
        "cake",
        "curry",
        "soup",
        "salad",
        "restaurant",
        "menu",
        "logo",
        "illustration",
        "painting",
        "drawing",
        "poster",
        "advertisement",
        "packaging",
        "bottle",
        "field",
        "plant",
        "leaf",
        "leaves",
    }

    for bad in bad_words:

        if bad in title_tokens:

            # Some foods legitimately appear in dishes.
            # But for raw ingredients we want the actual food.
            if food_name in {
                "Apple",
                "Banana",
                "Mango",
                "Orange",
                "Papaya",
                "Guava",
                "Pomegranate",
                "Watermelon",
                "Grapes",
                "Carrot",
                "Beetroot",
                "Broccoli",
                "Cauliflower",
                "Tomato",
                "Spinach",
                "Okra (Bhindi)",
                "Bottle Gourd",
                "Sweet Potato",
            }:
                best_score -= 250

    return best_score


# ------------------------------------------------------------
# ACCEPTANCE RULE
# ------------------------------------------------------------

def is_acceptable(food_name: str, title: str, score: int):

    if score < 500:
        return False

    title_norm = normalize(title)

    aliases = ALIASES.get(food_name, [])

    base = re.sub(r"\([^)]*\)", "", food_name).strip()

    candidates = [base] + aliases

    candidates = [
        normalize(x)
        for x in candidates
        if x
    ]

    # Must contain at least one strong expected phrase
    strong_match = False

    for candidate in candidates:

        if candidate == title_norm:
            strong_match = True
            break

        if f" {candidate} " in f" {title_norm} ":
            strong_match = True
            break

    if not strong_match:

        expected_tokens = set()

        for candidate in candidates:
            expected_tokens.update(candidate.split())

        title_tokens = tokens(title)

        if not expected_tokens:
            return False

        overlap = len(
            expected_tokens.intersection(title_tokens)
        )

        ratio = overlap / len(expected_tokens)

        if ratio < 0.75:
            return False

    return True


# ------------------------------------------------------------
# HTTP REQUEST
# ------------------------------------------------------------

async def commons_request(session, params, retries=5):

    for attempt in range(retries):

        try:

            async with session.get(
                COMMONS_API,
                params=params,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:

                if response.status == 429:

                    wait = min(
                        10 * (attempt + 1),
                        60
                    )

                    print(
                        f"  Rate limited. Waiting {wait}s..."
                    )

                    await asyncio.sleep(wait)

                    continue

                response.raise_for_status()

                return await response.json()

        except Exception as exc:

            if attempt == retries - 1:
                print(f"  Request failed: {exc}")
                return None

            wait = 3 * (attempt + 1)

            print(
                f"  Request error. Retrying in {wait}s..."
            )

            await asyncio.sleep(wait)

    return None


# ------------------------------------------------------------
# SEARCH COMMONS
# ------------------------------------------------------------

async def search_commons(session, food_name):

    search_terms = get_search_terms(food_name)

    all_results = {}

    for search_term in search_terms:

        print(
            f"  Searching Commons: {search_term}"
        )

        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": (
                f"intitle:{search_term}"
            ),
            "gsrnamespace": 6,
            "gsrlimit": 10,
            "prop": "imageinfo",
            "iiprop": (
                "url|size|mime|extmetadata"
            ),
            "iiurlwidth": 1000,
            "format": "json",
            "formatversion": 2,
        }

        data = await commons_request(
            session,
            params,
        )

        if not data:
            continue

        pages = data.get(
            "query",
            {}
        ).get(
            "pages",
            []
        )

        for page in pages:

            pageid = page.get("pageid")

            if pageid:
                all_results[pageid] = page

        # Be polite to Commons
        await asyncio.sleep(2)

    return list(all_results.values())


# ------------------------------------------------------------
# FIND BEST IMAGE
# ------------------------------------------------------------

async def find_best_image(session, food_name):

    pages = await search_commons(
        session,
        food_name,
    )

    candidates = []

    for page in pages:

        title = page.get(
            "title",
            ""
        )

        imageinfo = page.get(
            "imageinfo",
            []
        )

        if not imageinfo:
            continue

        info = imageinfo[0]

        mime = info.get(
            "mime",
            ""
        )

        if not mime.startswith("image/"):
            continue

        width = info.get(
            "width",
            0
        )

        height = info.get(
            "height",
            0
        )

        if width < 300 or height < 300:
            continue

        score = score_result(
            food_name,
            title,
        )

        if not is_acceptable(
            food_name,
            title,
            score,
        ):
            continue

        candidates.append(
            {
                "title": title,
                "score": score,
                "url": info.get("thumburl")
                or info.get("url"),
                "source_url": (
                    "https://commons.wikimedia.org/wiki/"
                    + quote(
                        title.replace(
                            "File:",
                            "File:"
                        ).replace(
                            " ",
                            "_"
                        ),
                        safe=":/_"
                    )
                ),
                "width": width,
                "height": height,
                "mime": mime,
                "metadata": info.get(
                    "extmetadata",
                    {}
                ),
            }
        )

    if not candidates:
        return None

    candidates.sort(
        key=lambda x: (
            x["score"],
            x["width"] * x["height"],
        ),
        reverse=True,
    )

    return candidates[0]


# ------------------------------------------------------------
# DOWNLOAD
# ------------------------------------------------------------

async def download_image(
    session,
    url,
    output_path,
):

    try:

        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=60),
        ) as response:

            response.raise_for_status()

            content = await response.read()

            if len(content) < 10_000:
                print(
                    "  Rejected: image too small."
                )
                return False

            output_path.write_bytes(content)

            return True

    except Exception as exc:

        print(
            f"  Download failed: {exc}"
        )

        return False


# ------------------------------------------------------------
# METADATA HELPER
# ------------------------------------------------------------

def metadata_value(metadata, key):

    value = metadata.get(key, {})

    if isinstance(value, dict):
        return value.get("value", "")

    return value


# ------------------------------------------------------------
# PROCESS ONE FOOD
# ------------------------------------------------------------

async def process_food(
    session,
    db,
    food,
    index,
    total,
):

    food_name = food["name"]

    slug = slugify(food_name)

    output_path = IMAGE_DIR / f"{slug}.jpg"

    print()
    print(
        f"[{index:02d}/{total}] {food_name}"
    )

    # --------------------------------------------------------
    # Already downloaded
    # --------------------------------------------------------

    if (
        output_path.exists()
        and output_path.stat().st_size > 10_000
    ):

        print(
            "  Already exists — skipping."
        )

        await db.foods.update_one(
            {"id": food["id"]},
            {
                "$set": {
                    "image_url": (
                        f"/images/food/items/{slug}.jpg"
                    ),
                }
            },
        )

        return "existing"

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    best = await find_best_image(
        session,
        food_name,
    )

    if not best:

        print(
            "  NO SAFE MATCH — skipped."
        )

        return "skipped"

    print(
        f"  Match: {best['title']}"
    )

    print(
        f"  Score: {best['score']}"
    )

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    ok = await download_image(
        session,
        best["url"],
        output_path,
    )

    if not ok:

        if output_path.exists():
            output_path.unlink()

        return "failed"

    # --------------------------------------------------------
    # Attribution
    # --------------------------------------------------------

    metadata = best.get(
        "metadata",
        {}
    )

    artist = metadata_value(
        metadata,
        "Artist",
    )

    license_name = metadata_value(
        metadata,
        "LicenseShortName",
    )

    license_url = metadata_value(
        metadata,
        "LicenseUrl",
    )

    # --------------------------------------------------------
    # SAVE TO MONGODB
    # --------------------------------------------------------

    await db.foods.update_one(
        {"id": food["id"]},
        {
            "$set": {
                "image_url": (
                    f"/images/food/items/{slug}.jpg"
                ),
                "image_source": "Wikimedia Commons",
                "image_source_url": best[
                    "source_url"
                ],
                "image_title": best[
                    "title"
                ],
                "image_author": artist,
                "image_license": license_name,
                "image_license_url": license_url,
                "image_match_score": best[
                    "score"
                ],
            }
        },
    )

    print(
        "  DOWNLOADED REAL PHOTO"
    )

    return "downloaded"


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

async def main():

    print("=" * 70)
    print(
        "DEHA VEDA — FREE REAL FOOD PHOTO IMPORTER"
    )
    print("=" * 70)

    print()
    print(
        "Source : Wikimedia Commons"
    )

    print(
        "Cost   : ₹0"
    )

    print(
        f"Images : {IMAGE_DIR}"
    )

    print()

    # --------------------------------------------------------
    # MongoDB
    # --------------------------------------------------------

    client = AsyncIOMotorClient(
        MONGO_URL
    )

    db = client[DB_NAME]

    foods = await db.foods.find(
        {},
        {
            "_id": 0
        },
    ).sort(
        "name",
        1,
    ).to_list(200)

    print(
        f"Foods found: {len(foods)}"
    )

    print()

    if not foods:

        print(
            "ERROR: No foods found in MongoDB."
        )

        client.close()

        return

    # --------------------------------------------------------
    # HTTP SESSION
    # --------------------------------------------------------

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    connector = aiohttp.TCPConnector(
        limit=2
    )

    async with aiohttp.ClientSession(
        headers=headers,
        connector=connector,
    ) as session:

        downloaded = 0
        existing = 0
        skipped = 0
        failed = 0

        total = len(foods)

        for index, food in enumerate(
            foods,
            start=1,
        ):

            result = await process_food(
                session,
                db,
                food,
                index,
                total,
            )

            if result == "downloaded":
                downloaded += 1

            elif result == "existing":
                existing += 1

            elif result == "skipped":
                skipped += 1

            elif result == "failed":
                failed += 1

            # ------------------------------------------------
            # IMPORTANT:
            # Slow requests prevent Wikimedia rate limiting.
            # ------------------------------------------------

            await asyncio.sleep(3)

    client.close()

    print()
    print("=" * 70)
    print("IMPORT COMPLETE")
    print("=" * 70)

    print(
        f"Real photos downloaded : {downloaded}"
    )

    print(
        f"Already existed        : {existing}"
    )

    print(
        f"Skipped (unsafe match) : {skipped}"
    )

    print(
        f"Failed                 : {failed}"
    )

    print()

    print(
        "Images directory:"
    )

    print(
        IMAGE_DIR
    )

    print()

    print(
        "MongoDB image_url fields updated."
    )

    print(
        "Attribution/license metadata stored."
    )

    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())