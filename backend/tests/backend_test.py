"""Deha Veda Ecosystem — backend API regression suite."""
import time
import uuid

import pytest
import requests

from conftest import API, BASE_URL, new_user


# ---------------- health / public content ----------------
class TestPublicContent:
    def test_root(self, api_client):
        r = api_client.get(f"{API}/")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_community_stats_shape(self, api_client):
        r = api_client.get(f"{API}/stats/community")
        assert r.status_code == 200
        d = r.json()
        for k in ("community_members", "foods_catalogued"):
            assert isinstance(d[k], int), f"{k} not int"
        assert d["foods_catalogued"] >= 60, d

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
        # premium field should be stripped from responses
        assert all("premium" not in i for i in d["items"])

    def test_food_search(self, api_client):
        r = api_client.get(f"{API}/foods", params={"q": "Apple"})
        assert r.status_code == 200
        items = r.json()["items"]
        assert items and any("apple" in i["name"].lower() for i in items)
        food = items[0]
        for k in ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g"):
            assert k in food, f"missing {k}"

    def test_food_search_no_results(self, api_client):
        r = api_client.get(f"{API}/foods", params={"q": "zzzqqq"})
        assert r.status_code == 200
        assert r.json()["items"] == []

    def test_food_category_filter(self, api_client):
        r = api_client.get(f"{API}/foods", params={"category": "Fruits"})
        assert r.status_code == 200
        items = r.json()["items"]
        assert items
        assert all(i["category"] == "Fruits" for i in items)

    @pytest.mark.parametrize("path,keys", [
        ("/jala", ["water_types", "journey", "parameters", "contamination", "gallery"]),
        ("/manas", ["topics", "brain_regions", "peaceful_mind"]),
    ])
    def test_pillar_endpoints(self, api_client, path, keys):
        r = api_client.get(f"{API}{path}")
        assert r.status_code == 200
        d = r.json()
        for k in keys:
            assert d.get(k), f"{path} missing/empty {k}"

    def test_jala_journey_has_nine_steps_all_unlocked(self, api_client):
        d = api_client.get(f"{API}/jala").json()
        assert len(d["journey"]) == 9, len(d["journey"])
        assert len(d["parameters"]) >= 10
        assert not any(p.get("locked") for p in d["parameters"]), "should all be unlocked"
        assert all(p.get("reference") or p.get("safe_range") for p in d["parameters"])
        assert not any(w.get("locked") for w in d["water_types"])
        assert len(d["water_types"]) >= 12

    def test_manas_all_topics_unlocked(self, api_client):
        d = api_client.get(f"{API}/manas").json()
        assert len(d["topics"]) == 12, len(d["topics"])
        assert not any(t.get("locked") for t in d["topics"])


# ---------------- calorie tool ----------------
class TestCalorieTool:
    def test_calorie_male_moderate_lose(self, api_client):
        payload = {"age": 30, "sex": "male", "height_cm": 175, "weight_kg": 70,
                   "activity": "moderate", "goal": "lose"}
        r = api_client.post(f"{API}/tools/calorie", json=payload)
        assert r.status_code == 200
        d = r.json()
        expected_bmr = round(10 * 70 + 6.25 * 175 - 5 * 30 + 5)
        assert d["bmr"] == expected_bmr, d
        assert d["maintenance"] == round(expected_bmr * 1.55)
        assert d["goal_range"] == [round(expected_bmr * 1.55) - 500, round(expected_bmr * 1.55) - 250]
        assert d["bmi"] == 22.9
        assert "not medical" in d["disclaimer"].lower()

    @pytest.mark.parametrize("bad", [
        {"age": 5, "sex": "male", "height_cm": 175, "weight_kg": 70, "activity": "moderate", "goal": "lose"},
        {"age": 30, "sex": "other", "height_cm": 175, "weight_kg": 70, "activity": "moderate", "goal": "lose"},
        {"age": 30, "sex": "male", "height_cm": 175, "weight_kg": 70, "activity": "hyper", "goal": "lose"},
    ])
    def test_calorie_validation(self, api_client, bad):
        assert api_client.post(f"{API}/tools/calorie", json=bad).status_code == 422


# ---------------- auth ----------------
class TestAuth:
    def test_register_increments_community_count(self, api_client):
        before = api_client.get(f"{API}/stats/community").json()["community_members"]
        client, user, _ = new_user()
        after = api_client.get(f"{API}/stats/community").json()["community_members"]
        assert after == before + 1, f"before={before} after={after}"
        assert user["role"] == "user"
        # premium field should no longer be present
        assert "premium" not in user

    def test_register_short_password_rejected(self, api_client):
        r = api_client.post(f"{API}/auth/register", json={
            "name": "TEST_Short", "email": f"test_{uuid.uuid4().hex[:8]}@dvtest.com", "password": "abc12"})
        assert r.status_code == 422

    def test_register_duplicate_email(self, api_client, class_user):
        _, user, password = class_user
        r = api_client.post(f"{API}/auth/register",
                            json={"name": "TEST_Dup", "email": user["email"], "password": password})
        assert r.status_code == 400
        assert "exists" in r.json()["detail"].lower()

    def test_login_sets_httponly_cookies_and_token(self, api_client, class_user):
        _, user, password = class_user
        r = api_client.post(f"{API}/auth/login", json={"email": user["email"], "password": password})
        assert r.status_code == 200
        assert r.json()["token"]
        set_cookies = r.headers.get("set-cookie", "").lower()
        assert "access_token" in set_cookies, r.headers
        assert "httponly" in set_cookies, set_cookies
        assert "samesite=none" in set_cookies and "secure" in set_cookies, set_cookies

    def test_login_invalid_password_401_string_detail(self, api_client, class_user):
        _, user, _ = class_user
        r = api_client.post(f"{API}/auth/login", json={"email": user["email"], "password": "WrongPass@123"})
        assert r.status_code == 401
        assert isinstance(r.json()["detail"], str)

    def test_me_requires_auth(self, api_client):
        assert api_client.get(f"{API}/auth/me").status_code == 401

    def test_me_returns_user_without_password(self, class_user):
        client, user, _ = class_user
        r = client.get(f"{API}/auth/me")
        assert r.status_code == 200
        d = r.json()
        assert d["email"] == user["email"]
        assert "password_hash" not in d and "_id" not in d

    def test_zz_brute_force_lockout_after_5_failures(self, api_client, class_user):
        # runs last in this class: locks out the shared class user for 15 minutes
        _, user, _ = class_user
        statuses = []
        for _ in range(8):
            r = api_client.post(f"{API}/auth/login", json={"email": user["email"], "password": "Nope@12345"})
            statuses.append(r.status_code)
            if r.status_code == 429:
                break
        assert 429 in statuses, f"no lockout: {statuses}"
        assert statuses.index(429) <= 5, statuses
        assert all(s == 401 for s in statuses[:statuses.index(429)]), statuses

    def test_logout_clears_cookies(self, class_user):
        client, _, _ = class_user
        r = client.post(f"{API}/auth/logout")
        assert r.status_code == 200
        assert r.json()["ok"] is True


# ---------------- iteration 2 fixes: lockout key + /api/track ----------------
class TestLockoutAndTracking:
    def test_successful_login_clears_failed_counter(self, api_client):
        client, user, password = new_user()
        email = user["email"]
        for i in range(4):
            r = api_client.post(f"{API}/auth/login", json={"email": email, "password": "Bad@12345"})
            assert r.status_code == 401, (i, r.status_code)
        ok = api_client.post(f"{API}/auth/login", json={"email": email, "password": password})
        assert ok.status_code == 200, ok.text[:200]
        for i in range(4):
            r = api_client.post(f"{API}/auth/login", json={"email": email, "password": "Bad@12345"})
            assert r.status_code == 401, f"counter not cleared after success (attempt {i}): {r.status_code}"
        assert client.get(f"{API}/auth/me").status_code == 200

    def test_track_accepts_json_body(self, api_client):
        r = api_client.post(f"{API}/track", json={"path": "/qa-track-test"})
        assert r.status_code == 200, r.text[:200]

    @pytest.mark.parametrize("bad", [{}, {"path": ""}, {"path": 123}, {"other": "x"}])
    def test_track_rejects_invalid_body(self, api_client, bad):
        r = api_client.post(f"{API}/track", json=bad)
        assert r.status_code == 422, f"body={bad} -> {r.status_code}"

    def test_track_shows_up_in_admin_popular_pages(self, api_client, admin_client):
        marker = f"/qa-popular-{uuid.uuid4().hex[:6]}"
        for _ in range(3):
            assert api_client.post(f"{API}/track", json={"path": marker}).status_code == 200
        time.sleep(1)
        d = admin_client.get(f"{API}/admin/stats").json()
        pages = d.get("popular_pages")
        assert isinstance(pages, list) and pages, f"popular_pages empty: {pages}"
        assert all("path" in p and "views" in p for p in pages), pages[:3]
        assert any(p["views"] >= 1 for p in pages)

    def test_register_rate_limit_allows_multiple(self, api_client):
        for _ in range(3):
            r = api_client.post(f"{API}/auth/register", json={
                "name": "TEST_RL", "email": f"test_{uuid.uuid4().hex[:10]}@dvtest.com",
                "password": "TestPass@2026"})
            assert r.status_code == 200, r.text[:200]


# ---------------- contact ----------------
class TestContact:
    def test_contact_valid(self, api_client):
        payload = {"name": "TEST_Contact", "email": "test_contact@dvtest.com",
                   "subject": "Testing subject", "message": "This is a test message of enough length."}
        r = api_client.post(f"{API}/contact", json=payload)
        assert r.status_code == 200, r.text[:200]
        assert r.json()["received"] is True

    @pytest.mark.parametrize("bad", [
        {"name": "A", "email": "a@b.com", "subject": "Hello", "message": "long enough message here"},
        {"name": "Valid Name", "email": "notanemail", "subject": "Hello", "message": "long enough message here"},
        {"name": "Valid Name", "email": "a@b.com", "subject": "Hi", "message": "long enough message here"},
        {"name": "Valid Name", "email": "a@b.com", "subject": "Hello", "message": "short"},
    ])
    def test_contact_validation(self, api_client, bad):
        assert api_client.post(f"{API}/contact", json=bad).status_code == 422


# ---------------- admin ----------------
class TestAdmin:
    def test_admin_endpoints_require_admin(self, api_client, session_user):
        client, _, _ = session_user
        for path in ("/admin/stats", "/admin/users", "/admin/contact"):
            assert api_client.get(f"{API}{path}").status_code == 401, path
            assert client.get(f"{API}{path}").status_code == 403, path

    def test_admin_stats(self, admin_client):
        r = admin_client.get(f"{API}/admin/stats")
        assert r.status_code == 200, r.text[:300]
        d = r.json()
        for k in ("total_users", "new_registrations_7d", "contact_messages", "ai_messages"):
            assert k in d, k
        assert len(d["registrations_7d"]) == 7
        assert all("day" in x and "users" in x for x in d["registrations_7d"])
        # removed fields must not be present
        for removed in ("active_subscribers", "game_activity", "revenue", "pending_claims"):
            assert removed not in d, f"removed field still present: {removed}"

    def test_admin_users_list(self, admin_client):
        r = admin_client.get(f"{API}/admin/users")
        assert r.status_code == 200
        users = r.json()["users"]
        assert users and "password_hash" not in users[0] and "_id" not in users[0]

    def test_admin_contact_messages(self, admin_client, api_client):
        subject = f"TEST_subject_{uuid.uuid4().hex[:6]}"
        api_client.post(f"{API}/contact", json={
            "name": "TEST_Msg", "email": "test_msg@dvtest.com", "subject": subject,
            "message": "Message body long enough for validation."})
        msgs = admin_client.get(f"{API}/admin/contact").json()["messages"]
        assert any(m["subject"] == subject for m in msgs), "contact message not visible to admin"

    def test_admin_food_crud_and_search(self, admin_client, api_client):
        name = f"TEST_Food_{uuid.uuid4().hex[:6]}"
        payload = {"name": name, "category": "Fruits", "serving_size": "100 g", "calories": 50,
                   "protein_g": 1, "carbs_g": 12, "fat_g": 0.2, "fiber_g": 2,
                   "micronutrients": "Vitamin C", "note": "test"}
        r = admin_client.post(f"{API}/admin/foods", json=payload)
        assert r.status_code == 200, r.text[:300]
        food_id = r.json()["id"]
        try:
            found = api_client.get(f"{API}/foods", params={"q": name}).json()["items"]
            assert found and found[0]["calories"] == 50
            # duplicate
            assert admin_client.post(f"{API}/admin/foods", json=payload).status_code == 400
            # update
            up = admin_client.put(f"{API}/admin/foods/{food_id}", json={**payload, "calories": 77})
            assert up.status_code == 200 and up.json()["calories"] == 77
            assert api_client.get(f"{API}/foods", params={"q": name}).json()["items"][0]["calories"] == 77
        finally:
            dr = admin_client.delete(f"{API}/admin/foods/{food_id}")
            assert dr.status_code == 200
        assert api_client.get(f"{API}/foods", params={"q": name}).json()["items"] == []
        assert admin_client.delete(f"{API}/admin/foods/{food_id}").status_code == 404


# ---------------- AI chat (SSE) ----------------
class TestAIChat:
    def test_anonymous_chat_streams_answer(self, api_client):
        session_id = str(uuid.uuid4())
        deltas = []
        with requests.post(f"{API}/chat", json={"message": "What is AHARA in one short sentence?",
                                                "session_id": session_id},
                           stream=True, timeout=120) as r:
            assert r.status_code == 200, r.text[:300]
            assert "text/event-stream" in r.headers.get("content-type", "")
            for line in r.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    import json as _json
                    payload = _json.loads(line[6:].strip())
                    assert "error" not in payload, payload
                    if "delta" in payload:
                        deltas.append(payload["delta"])
                    if payload.get("done"):
                        break
        answer = "".join(deltas)
        assert len(answer) > 20, f"empty/short AI answer: {answer!r}"

        time.sleep(1)
        hist = api_client.get(f"{API}/chat/history", params={"session_id": session_id})
        assert hist.status_code == 200
        msgs = hist.json()["messages"]
        assert len(msgs) >= 2 and msgs[0]["role"] == "user" and msgs[-1]["role"] == "assistant"

    def test_chat_validation(self, api_client):
        assert api_client.post(f"{API}/chat", json={"message": ""}).status_code == 422


# ---------------- security / infra ----------------
class TestSecurity:
    def test_bcrypt_hash_format(self):
        import subprocess
        out = subprocess.run(
            ["python", "-c",
             "import os,asyncio;from dotenv import load_dotenv;load_dotenv('/app/backend/.env');"
             "from motor.motor_asyncio import AsyncIOMotorClient;"
             "c=AsyncIOMotorClient(os.environ['MONGO_URL']);d=c[os.environ['DB_NAME']];"
             "print(asyncio.get_event_loop().run_until_complete("
             "d.users.find_one({'email':os.environ['ADMIN_EMAIL'].lower()}))['password_hash'])"],
            capture_output=True, text=True, timeout=60)
        assert out.returncode == 0, out.stderr[-500:]
        assert out.stdout.strip().startswith("$2b$"), out.stdout.strip()[:20]

    @pytest.mark.xfail(reason="k8s ingress rewrites Access-Control-Allow-Origin to '*' "
                              "(env-imposed; backend/.env has explicit CORS_ORIGINS)",
                       strict=False)
    def test_cors_allows_credentials_with_explicit_origin(self, api_client):
        r = api_client.options(f"{API}/auth/login", headers={
            "Origin": BASE_URL, "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"})
        assert r.status_code in (200, 204), r.status_code
        allow_origin = r.headers.get("access-control-allow-origin")
        assert allow_origin == BASE_URL, allow_origin
        assert r.headers.get("access-control-allow-credentials") == "true", dict(r.headers)
