import os
import uuid
from pathlib import Path

import pytest
import requests
from dotenv import dotenv_values


# ============================================================
# PROJECT PATHS
# ============================================================

TESTS_DIR = Path(__file__).resolve().parent
BACKEND_DIR = TESTS_DIR.parent
PROJECT_ROOT = BACKEND_DIR.parent

FRONTEND_ENV = PROJECT_ROOT / "frontend" / ".env"


# ============================================================
# BACKEND URL
# ============================================================

frontend_env = dotenv_values(FRONTEND_ENV)

base_url = (
    os.environ.get("REACT_APP_BACKEND_URL")
    or frontend_env.get("REACT_APP_BACKEND_URL")
)

if not base_url:
    raise RuntimeError(
        "REACT_APP_BACKEND_URL is missing. "
        "Set it in the environment or frontend/.env"
    )

BASE_URL = base_url.rstrip("/")
API = f"{BASE_URL}/api"


# ============================================================
# ADMIN CREDENTIALS
# ============================================================

def _creds():
    """
    Read admin test credentials from environment variables.

    Required:
        TEST_ADMIN_EMAIL
        TEST_ADMIN_PASSWORD
    """

    email = os.environ.get("TEST_ADMIN_EMAIL")
    password = os.environ.get("TEST_ADMIN_PASSWORD")

    if not email or not password:
        return [], []

    return [email], [password]


@pytest.fixture(scope="session")
def admin_credentials():
    emails, passwords = _creds()

    if not emails or not passwords:
        pytest.skip(
            "TEST_ADMIN_EMAIL and TEST_ADMIN_PASSWORD "
            "environment variables are not configured."
        )

    return {
        "email": emails[0],
        "password": passwords[0],
    }


# ============================================================
# API CLIENT
# ============================================================

@pytest.fixture
def api_client():
    session = requests.Session()

    session.headers.update({
        "Content-Type": "application/json"
    })

    return session


# ============================================================
# ADMIN CLIENT
# ============================================================

@pytest.fixture(scope="session")
def admin_client(admin_credentials):
    response = requests.post(
        f"{API}/auth/login",
        json=admin_credentials,
    )

    if response.status_code != 200:
        pytest.fail(
            f"Admin login failed "
            f"{response.status_code}: "
            f"{response.text[:300]}"
        )

    data = response.json()
    token = data.get("token")

    if not token:
        pytest.fail(
            f"Admin login succeeded but no token was returned: "
            f"{response.text[:300]}"
        )

    session = requests.Session()

    session.headers.update({
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    })

    return session


# ============================================================
# TEST USER
# ============================================================

def new_user():
    """
    Register a fresh test user.

    Returns:
        (client, user_dict, password)
    """

    email = f"test_{uuid.uuid4().hex[:10]}@dvtest.com"
    password = "TestPass@2026"

    response = requests.post(
        f"{API}/auth/register",
        json={
            "name": "TEST_User",
            "email": email,
            "password": password,
        },
    )

    if response.status_code != 200:
        pytest.fail(
            f"Register failed "
            f"{response.status_code}: "
            f"{response.text[:300]}"
        )

    data = response.json()

    token = data.get("token")
    user = data.get("user")

    if not token:
        pytest.fail(
            f"Registration succeeded but no token was returned: "
            f"{response.text[:300]}"
        )

    if not user:
        pytest.fail(
            f"Registration succeeded but no user was returned: "
            f"{response.text[:300]}"
        )

    session = requests.Session()

    session.headers.update({
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    })

    return session, user, password


# ============================================================
# CLASS-SCOPED TEST USER
# ============================================================

@pytest.fixture(scope="class")
def class_user():
    return new_user()


# ============================================================
# SESSION-SCOPED TEST USER
# ============================================================

@pytest.fixture(scope="session")
def session_user():
    return new_user()