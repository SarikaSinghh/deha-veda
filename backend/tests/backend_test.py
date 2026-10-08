"""Deha Veda Ecosystem — backend API regression suite."""

import json
import subprocess
import time
import uuid

import pytest
import requests

from conftest import API, BASE_URL, new_user


# ---------------- public content ----------------
class TestPublicContent:
    def test_root(self, api_client):
        r = api_client.get(f"{API}/")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_food_categories(self, api_client):
        r = api_client.get(f"{API}/foods/categories")
        assert r.status_code == 200
        assert len(r.json()["categories"]) > 3

    def test_foods_list_all_free(self, api_client):
        r = api_client.get(f"{API}/foods")
        assert r.status_code == 200

        d = r.json()

        assert d["is_premium"] is True
        assert d["total"] >= 60
        assert d["locked_count"] == 0, d["locked_count"]
        assert all(not i.get("locked") for i in d["items"])
        assert all("calories" in i for i in d["items"])

        # Premium field should be stripped from responses.
        assert all("premium" not in i for i in d["items"])

    def test_food_search(self, api_client):
        r = api_client.get(
            f"{API}/foods",
            params={"q": "Apple"},
        )

        assert r.status_code == 200

        items = r.json()["items"]
        assert items
        assert any("apple" in i["name"].lower() for i in items)

        food = items[0]

        for key in (
            "calories",
            "protein_g",
            "carbs_g",
            "fat_g",
            "fiber_g",
        ):
            assert key in food, f"missing {key}"

    def test_food_search_no_results(self, api_client):
        r = api_client.get(
            f"{API}/foods",
            params={"q": "zzzqqq"},
        )

        assert r.status_code == 200
        assert r.json()["items"] == []

    def test_food_category_filter(self, api_client):
        r = api_client.get(
            f"{API}/foods",
            params={"category": "Fruits"},
        )

        assert r.status_code == 200

        items = r.json()["items"]

        assert items
        assert all(i["category"] == "Fruits" for i in items)

    @pytest.mark.parametrize(
        "path,keys",
        [
            (
                "/jala",
                [
                    "water_types",
                    "journey",
                    "parameters",
                    "contamination",
                    "gallery",
                ],
            ),
            (
                "/manas",
                [
                    "topics",
                    "brain_regions",
                    "peaceful_mind",
                ],
            ),
        ],
    )
    def test_pillar_endpoints(self, api_client, path, keys):
        r = api_client.get(f"{API}{path}")

        assert r.status_code == 200

        data = r.json()

        for key in keys:
            assert data.get(key), f"{path} missing/empty {key}"

    def test_jala_journey_has_nine_steps_all_unlocked(self, api_client):
        data = api_client.get(f"{API}/jala").json()

        assert len(data["journey"]) == 9, len(data["journey"])
        assert len(data["parameters"]) >= 10

        assert not any(
            parameter.get("locked")
            for parameter in data["parameters"]
        ), "should all be unlocked"

        assert all(
            parameter.get("reference")
            or parameter.get("safe_range")
            for parameter in data["parameters"]
        )

        assert not any(
            water_type.get("locked")
            for water_type in data["water_types"]
        )

        assert len(data["water_types"]) >= 12

    def test_manas_all_topics_unlocked(self, api_client):
        data = api_client.get(f"{API}/manas").json()

        assert len(data["topics"]) == 12, len(data["topics"])

        assert not any(
            topic.get("locked")
            for topic in data["topics"]
        )


# ---------------- community / catalog stats ----------------
class TestCommunityStats:
    def test_food_catalogue_stats(self, api_client):
        r = api_client.get(f"{API}/stats/community")

        assert r.status_code == 200

        data = r.json()

        assert "foods_catalogued" in data
        assert isinstance(data["foods_catalogued"], int)
        assert data["foods_catalogued"] >= 60

        # Community member count was intentionally removed.
        assert "community_members" not in data


# ---------------- calorie tool ----------------
class TestCalorieTool:
    def test_calorie_male_moderate_lose(self, api_client):
        payload = {
            "age": 30,
            "sex": "male",
            "height_cm": 175,
            "weight_kg": 70,
            "activity": "moderate",
            "goal": "lose",
        }

        r = api_client.post(
            f"{API}/tools/calorie",
            json=payload,
        )

        assert r.status_code == 200

        data = r.json()

        expected_bmr = round(
            10 * 70
            + 6.25 * 175
            - 5 * 30
            + 5
        )

        assert data["bmr"] == expected_bmr, data
        assert data["maintenance"] == round(
            expected_bmr * 1.55
        )

        assert data["goal_range"] == [
            round(expected_bmr * 1.55) - 500,
            round(expected_bmr * 1.55) - 250,
        ]

        assert data["bmi"] == 22.9
        assert "not medical" in data["disclaimer"].lower()

    @pytest.mark.parametrize(
        "bad",
        [
            {
                "age": 5,
                "sex": "male",
                "height_cm": 175,
                "weight_kg": 70,
                "activity": "moderate",
                "goal": "lose",
            },
            {
                "age": 30,
                "sex": "other",
                "height_cm": 175,
                "weight_kg": 70,
                "activity": "moderate",
                "goal": "lose",
            },
            {
                "age": 30,
                "sex": "male",
                "height_cm": 175,
                "weight_kg": 70,
                "activity": "hyper",
                "goal": "lose",
            },
        ],
    )
    def test_calorie_validation(self, api_client, bad):
        r = api_client.post(
            f"{API}/tools/calorie",
            json=bad,
        )

        assert r.status_code == 422


# ---------------- auth ----------------
class TestAuth:
    def test_register_short_password_rejected(self, api_client):
        r = api_client.post(
            f"{API}/auth/register",
            json={
                "name": "TEST_Short",
                "email": (
                    f"test_{uuid.uuid4().hex[:8]}"
                    "@dvtest.com"
                ),
                "password": "abc12",
            },
        )

        assert r.status_code == 422

    def test_register_duplicate_email(self, api_client, class_user):
        _, user, password = class_user

        r = api_client.post(
            f"{API}/auth/register",
            json={
                "name": "TEST_Dup",
                "email": user["email"],
                "password": password,
            },
        )

        assert r.status_code == 400
        assert "exists" in r.json()["detail"].lower()

    def test_login_sets_httponly_cookies_and_token(
        self,
        api_client,
        class_user,
    ):
        _, user, password = class_user

        r = api_client.post(
            f"{API}/auth/login",
            json={
                "email": user["email"],
                "password": password,
            },
        )

        assert r.status_code == 200
        assert r.json()["token"]

        set_cookies = r.headers.get(
            "set-cookie",
            "",
        ).lower()

        assert "access_token" in set_cookies, r.headers
        assert "httponly" in set_cookies, set_cookies
        assert (
            "samesite=none" in set_cookies
            and "secure" in set_cookies
        ), set_cookies

    def test_login_invalid_password_401_string_detail(
        self,
        api_client,
        class_user,
    ):
        _, user, _ = class_user

        r = api_client.post(
            f"{API}/auth/login",
            json={
                "email": user["email"],
                "password": "WrongPass@123",
            },
        )

        assert r.status_code == 401
        assert isinstance(r.json()["detail"], str)

    def test_me_requires_auth(self, api_client):
        r = api_client.get(f"{API}/auth/me")

        assert r.status_code == 401

    def test_me_returns_user_without_password(self, class_user):
        client, user, _ = class_user

        r = client.get(f"{API}/auth/me")

        assert r.status_code == 200

        data = r.json()

        assert data["email"] == user["email"]
        assert "password_hash" not in data
        assert "_id" not in data

    def test_zz_brute_force_lockout_after_5_failures(
        self,
        api_client,
        class_user,
    ):
        # Runs last in this class because it locks the shared
        # class user for approximately 15 minutes.
        _, user, _ = class_user

        statuses = []

        for _ in range(8):
            r = api_client.post(
                f"{API}/auth/login",
                json={
                    "email": user["email"],
                    "password": "Nope@12345",
                },
            )

            statuses.append(r.status_code)

            if r.status_code == 429:
                break

        assert 429 in statuses, (
            f"no lockout: {statuses}"
        )

        lockout_index = statuses.index(429)

        assert lockout_index <= 5, statuses

        assert all(
            status == 401
            for status in statuses[:lockout_index]
        ), statuses

    def test_logout_clears_cookies(self, class_user):
        client, _, _ = class_user

        r = client.post(f"{API}/auth/logout")

        assert r.status_code == 200
        assert r.json()["ok"] is True


# ---------------- lockout + tracking ----------------
class TestLockoutAndTracking:
    def test_successful_login_clears_failed_counter(
        self,
        api_client,
    ):
        client, user, password = new_user()
        email = user["email"]

        for i in range(4):
            r = api_client.post(
                f"{API}/auth/login",
                json={
                    "email": email,
                    "password": "Bad@12345",
                },
            )

            assert r.status_code == 401, (
                i,
                r.status_code,
            )

        ok = api_client.post(
            f"{API}/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        assert ok.status_code == 200, ok.text[:200]

        for i in range(4):
            r = api_client.post(
                f"{API}/auth/login",
                json={
                    "email": email,
                    "password": "Bad@12345",
                },
            )

            assert r.status_code == 401, (
                f"counter not cleared after success "
                f"(attempt {i}): {r.status_code}"
            )

        assert client.get(
            f"{API}/auth/me"
        ).status_code == 200

    def test_track_accepts_json_body(self, api_client):
        r = api_client.post(
            f"{API}/track",
            json={"path": "/qa-track-test"},
        )

        assert r.status_code == 200, r.text[:200]

    @pytest.mark.parametrize(
        "bad",
        [
            {},
            {"path": ""},
            {"path": 123},
            {"other": "x"},
        ],
    )
    def test_track_rejects_invalid_body(
        self,
        api_client,
        bad,
    ):
        r = api_client.post(
            f"{API}/track",
            json=bad,
        )

        assert r.status_code == 422, (
            f"body={bad} -> {r.status_code}"
        )

    def test_track_shows_up_in_admin_popular_pages(
        self,
        api_client,
        admin_client,
    ):
        marker = (
            f"/qa-popular-"
            f"{uuid.uuid4().hex[:6]}"
        )

        for _ in range(3):
            r = api_client.post(
                f"{API}/track",
                json={"path": marker},
            )

            assert r.status_code == 200

        time.sleep(1)

        r = admin_client.get(f"{API}/admin/stats")

        assert r.status_code == 200

        data = r.json()
        pages = data.get("popular_pages")

        assert isinstance(pages, list) and pages, (
            f"popular_pages empty: {pages}"
        )

        assert all(
            "path" in page and "views" in page
            for page in pages
        ), pages[:3]

        assert any(
            page["views"] >= 1
            for page in pages
        )

    def test_register_rate_limit_allows_multiple(
        self,
        api_client,
    ):
        for _ in range(3):
            r = api_client.post(
                f"{API}/auth/register",
                json={
                    "name": "TEST_RL",
                    "email": (
                        f"test_{uuid.uuid4().hex[:10]}"
                        "@dvtest.com"
                    ),
                    "password": "TestPass@2026",
                },
            )

            assert r.status_code == 200, r.text[:200]


# ---------------- contact ----------------
class TestContact:
    def test_contact_valid(self, api_client):
        payload = {
            "name": "TEST_Contact",
            "email": "test_contact@dvtest.com",
            "subject": "Testing subject",
            "message": (
                "This is a test message of enough length."
            ),
        }

        r = api_client.post(
            f"{API}/contact",
            json=payload,
        )

        assert r.status_code == 200, r.text[:200]
        assert r.json()["received"] is True

    @pytest.mark.parametrize(
        "bad",
        [
            {
                "name": "A",
                "email": "a@b.com",
                "subject": "Hello",
                "message": "long enough message here",
            },
            {
                "name": "Valid Name",
                "email": "notanemail",
                "subject": "Hello",
                "message": "long enough message here",
            },
            {
                "name": "Valid Name",
                "email": "a@b.com",
                "subject": "Hi",
                "message": "long enough message here",
            },
            {
                "name": "Valid Name",
                "email": "a@b.com",
                "subject": "Hello",
                "message": "short",
            },
        ],
    )
    def test_contact_validation(
        self,
        api_client,
        bad,
    ):
        r = api_client.post(
            f"{API}/contact",
            json=bad,
        )

        assert r.status_code == 422


# ---------------- admin ----------------
class TestAdmin:
    def test_admin_endpoints_require_admin(
        self,
        api_client,
        session_user,
    ):
        client, _, _ = session_user

        for path in (
            "/admin/stats",
            "/admin/users",
            "/admin/contact",
        ):
            assert (
                api_client.get(f"{API}{path}").status_code
                == 401
            ), path

            assert (
                client.get(f"{API}{path}").status_code
                == 403
            ), path

    def test_admin_stats(self, admin_client):
        r = admin_client.get(f"{API}/admin/stats")

        assert r.status_code == 200, r.text[:300]

        data = r.json()

        for key in (
            "total_users",
            "new_registrations_7d",
            "contact_messages",
            "ai_messages",
        ):
            assert key in data, key

        assert len(data["registrations_7d"]) == 7

        assert all(
            "day" in item and "users" in item
            for item in data["registrations_7d"]
        )

        # Removed subscription/game fields must not be present.
        for removed in (
            "active_subscribers",
            "game_activity",
            "revenue",
            "pending_claims",
        ):
            assert removed not in data, (
                f"removed field still present: {removed}"
            )

    def test_admin_users_list(self, admin_client):
        r = admin_client.get(f"{API}/admin/users")

        assert r.status_code == 200

        users = r.json()["users"]

        assert users
        assert "password_hash" not in users[0]
        assert "_id" not in users[0]

    def test_admin_contact_messages(
        self,
        admin_client,
        api_client,
    ):
        subject = (
            f"TEST_subject_"
            f"{uuid.uuid4().hex[:6]}"
        )

        r = api_client.post(
            f"{API}/contact",
            json={
                "name": "TEST_Msg",
                "email": "test_msg@dvtest.com",
                "subject": subject,
                "message": (
                    "Message body long enough "
                    "for validation."
                ),
            },
        )

        assert r.status_code == 200

        msgs = admin_client.get(
            f"{API}/admin/contact"
        ).json()["messages"]

        assert any(
            message["subject"] == subject
            for message in msgs
        ), "contact message not visible to admin"

    def test_admin_food_crud_and_search(
        self,
        admin_client,
        api_client,
    ):
        name = (
            f"TEST_Food_"
            f"{uuid.uuid4().hex[:6]}"
        )

        payload = {
            "name": name,
            "category": "Fruits",
            "serving_size": "100 g",
            "calories": 50,
            "protein_g": 1,
            "carbs_g": 12,
            "fat_g": 0.2,
            "fiber_g": 2,
            "micronutrients": "Vitamin C",
            "note": "test",
        }

        r = admin_client.post(
            f"{API}/admin/foods",
            json=payload,
        )

        assert r.status_code == 200, r.text[:300]

        food_id = r.json()["id"]

        try:
            found = api_client.get(
                f"{API}/foods",
                params={"q": name},
            ).json()["items"]

            assert found
            assert found[0]["calories"] == 50

            # Duplicate should be rejected.
            duplicate = admin_client.post(
                f"{API}/admin/foods",
                json=payload,
            )

            assert duplicate.status_code == 400

            # Update.
            updated = admin_client.put(
                f"{API}/admin/foods/{food_id}",
                json={
                    **payload,
                    "calories": 77,
                },
            )

            assert updated.status_code == 200
            assert updated.json()["calories"] == 77

            refreshed = api_client.get(
                f"{API}/foods",
                params={"q": name},
            ).json()["items"]

            assert refreshed[0]["calories"] == 77

        finally:
            delete_response = admin_client.delete(
                f"{API}/admin/foods/{food_id}"
            )

            assert delete_response.status_code == 200

        assert api_client.get(
            f"{API}/foods",
            params={"q": name},
        ).json()["items"] == []

        assert (
            admin_client.delete(
                f"{API}/admin/foods/{food_id}"
            ).status_code
            == 404
        )




# ---------------- security / infra ----------------
class TestSecurity:
    def test_bcrypt_hash_format(self):
        result = subprocess.run(
            [
                "python",
                "-c",
                (
                    "import os,asyncio;"
                    "from dotenv import load_dotenv;"
                    "load_dotenv('/app/backend/.env');"
                    "from motor.motor_asyncio import "
                    "AsyncIOMotorClient;"
                    "c=AsyncIOMotorClient(os.environ['MONGO_URL']);"
                    "d=c[os.environ['DB_NAME']];"
                    "print("
                    "asyncio.get_event_loop().run_until_complete("
                    "d.users.find_one("
                    "{'email':os.environ['ADMIN_EMAIL'].lower()}"
                    "))['password_hash'])"
                ),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode == 0, result.stderr[-500:]

        assert result.stdout.strip().startswith(
            "$2b$"
        ), result.stdout.strip()[:20]

    @pytest.mark.xfail(
        reason=(
            "k8s ingress rewrites "
            "Access-Control-Allow-Origin to '*' "
            "(env-imposed; backend/.env has explicit "
            "CORS_ORIGINS)"
        ),
        strict=False,
    )
    def test_cors_allows_credentials_with_explicit_origin(
        self,
        api_client,
    ):
        r = api_client.options(
            f"{API}/auth/login",
            headers={
                "Origin": BASE_URL,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )

        assert r.status_code in (200, 204), r.status_code

        allow_origin = r.headers.get(
            "access-control-allow-origin"
        )

        assert allow_origin == BASE_URL, allow_origin

        assert (
            r.headers.get(
                "access-control-allow-credentials"
            )
            == "true"
        ), dict(r.headers)