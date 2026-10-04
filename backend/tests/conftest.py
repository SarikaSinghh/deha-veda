import os
import re
import uuid
from pathlib import Path

import pytest
import requests
from dotenv import dotenv_values

frontend_env = dotenv_values("/app/frontend/.env")
base_url = os.environ.get("REACT_APP_BACKEND_URL") or frontend_env.get("REACT_APP_BACKEND_URL")
if not base_url:
    raise RuntimeError("REACT_APP_BACKEND_URL missing")
BASE_URL = base_url.rstrip("/")
API = f"{BASE_URL}/api"

# NOTE: backend applies rate_limit("reg:<ip>", 10, 3600) on /api/auth/register.
# Behind the shared ingress IP that means max 10 registrations per hour for the whole
# suite, so user-creating fixtures below are class/session scoped and reused.


def _creds():
    content = Path("/app/memory/test_credentials.md").read_text(encoding="utf-8")
    emails = re.findall(r'(?im)^\s*[-*]?\s*(?:\*\*)?Email(?:\*\*)?\s*:\s*`?([^`\s]+)', content)
    passwords = re.findall(r'(?im)^\s*[-*]?\s*(?:\*\*)?Password(?:\*\*)?\s*:\s*`?([^`\s]+)', content)
    return emails, passwords


@pytest.fixture(scope="session")
def admin_credentials():
    emails, passwords = _creds()
    if not emails or not passwords:
        pytest.skip("No credentials in /app/memory/test_credentials.md")
    return {"email": emails[0], "password": passwords[0]}


@pytest.fixture
def api_client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


@pytest.fixture(scope="session")
def admin_client(admin_credentials):
    r = requests.post(f"{API}/auth/login", json=admin_credentials)
    if r.status_code != 200:
        pytest.fail(f"Admin login failed {r.status_code}: {r.text[:300]}")
    token = r.json().get("token")
    assert token
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    return s


def new_user():
    """Register a fresh TEST_ user; returns (client, user_dict, password)."""
    email = f"test_{uuid.uuid4().hex[:10]}@dvtest.com"
    password = "TestPass@2026"
    r = requests.post(f"{API}/auth/register",
                      json={"name": "TEST_User", "email": email, "password": password})
    if r.status_code != 200:
        pytest.fail(f"Register failed {r.status_code}: {r.text[:300]}")
    data = r.json()
    client = requests.Session()
    client.headers.update({"Content-Type": "application/json",
                           "Authorization": f"Bearer {data['token']}"})
    return client, data["user"], password


@pytest.fixture(scope="class")
def class_user():
    return new_user()


@pytest.fixture(scope="session")
def session_user():
    return new_user()
