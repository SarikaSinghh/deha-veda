#!/usr/bin/env python3
"""
Backend API Test Suite for Deha Veda - Feature Removal Verification
Tests that Swara, Games, and Membership features have been completely removed
"""

import requests
import json
import uuid
from typing import Dict, Any, Optional

# Backend URL from frontend/.env
BASE_URL = "https://cleanup-plan-1.preview.emergentagent.com/api"

# Admin credentials from backend/.env
ADMIN_EMAIL = "admin@dehaveda.com"
ADMIN_PASSWORD = "DehaVeda@2026"

# Test results tracking
test_results = {
    "passed": [],
    "failed": [],
    "warnings": []
}


def log_pass(test_name: str, details: str = ""):
    """Log a passing test"""
    msg = f"✅ PASS: {test_name}"
    if details:
        msg += f" - {details}"
    print(msg)
    test_results["passed"].append({"test": test_name, "details": details})


def log_fail(test_name: str, details: str):
    """Log a failing test"""
    msg = f"❌ FAIL: {test_name} - {details}"
    print(msg)
    test_results["failed"].append({"test": test_name, "details": details})


def log_warning(test_name: str, details: str):
    """Log a warning"""
    msg = f"⚠️  WARNING: {test_name} - {details}"
    print(msg)
    test_results["warnings"].append({"test": test_name, "details": details})


def test_removed_endpoint(method: str, path: str, token: Optional[str] = None, data: Optional[Dict] = None):
    """Test that a removed endpoint returns 404 or 405"""
    url = f"{BASE_URL}{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data or {}, timeout=10)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data or {}, timeout=10)
        else:
            log_fail(f"Removed endpoint {method} {path}", f"Unsupported method: {method}")
            return
        
        if response.status_code in [404, 405]:
            log_pass(f"Removed endpoint {method} {path}", f"Returns {response.status_code} as expected")
        else:
            log_fail(f"Removed endpoint {method} {path}", 
                    f"Expected 404/405, got {response.status_code}: {response.text[:200]}")
    except Exception as e:
        log_fail(f"Removed endpoint {method} {path}", f"Request failed: {str(e)}")


def test_surviving_endpoint(method: str, path: str, expected_status: int = 200, 
                           token: Optional[str] = None, data: Optional[Dict] = None,
                           validation_func: Optional[callable] = None):
    """Test that a surviving endpoint works correctly"""
    url = f"{BASE_URL}{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data or {}, timeout=10)
        else:
            log_fail(f"Surviving endpoint {method} {path}", f"Unsupported method: {method}")
            return None
        
        if response.status_code != expected_status:
            log_fail(f"Surviving endpoint {method} {path}", 
                    f"Expected {expected_status}, got {response.status_code}: {response.text[:200]}")
            return None
        
        try:
            response_data = response.json()
        except:
            response_data = None
        
        if validation_func:
            validation_func(path, response_data)
        else:
            log_pass(f"Surviving endpoint {method} {path}", f"Returns {expected_status}")
        
        return response_data
    except Exception as e:
        log_fail(f"Surviving endpoint {method} {path}", f"Request failed: {str(e)}")
        return None


def validate_root(path: str, data: Dict):
    """Validate /api/ endpoint"""
    if data.get("status") == "ok":
        log_pass(f"GET {path}", "Returns status:ok")
    else:
        log_fail(f"GET {path}", f"Expected status:ok, got: {data}")


def validate_community_stats(path: str, data: Dict):
    """Validate /api/stats/community endpoint"""
    expected_fields = {"community_members", "foods_catalogued"}
    actual_fields = set(data.keys())
    
    if actual_fields == expected_fields:
        log_pass(f"GET {path}", f"Has ONLY {expected_fields}")
    else:
        extra = actual_fields - expected_fields
        missing = expected_fields - actual_fields
        details = []
        if extra:
            details.append(f"Extra fields: {extra}")
        if missing:
            details.append(f"Missing fields: {missing}")
        log_fail(f"GET {path}", " | ".join(details))


def validate_foods(path: str, data: Dict):
    """Validate /api/foods endpoint"""
    issues = []
    
    # Check is_premium is true
    if data.get("is_premium") != True:
        issues.append(f"is_premium should be true, got {data.get('is_premium')}")
    
    # Check all items have locked:false and no premium field
    items = data.get("items", [])
    if not items:
        issues.append("No items returned")
    
    for idx, item in enumerate(items[:5]):  # Check first 5 items
        if item.get("locked") != False:
            issues.append(f"Item {idx} has locked={item.get('locked')}, expected false")
        if "premium" in item:
            issues.append(f"Item {idx} has 'premium' field (should be removed)")
    
    if issues:
        log_fail(f"GET {path}", " | ".join(issues))
    else:
        log_pass(f"GET {path}", f"All {len(items)} items unlocked, no premium field, is_premium:true")


def validate_jala(path: str, data: Dict):
    """Validate /api/jala endpoint"""
    issues = []
    
    # Check is_premium is true
    if data.get("is_premium") != True:
        issues.append(f"is_premium should be true, got {data.get('is_premium')}")
    
    # Check water_types all have locked:false
    water_types = data.get("water_types", [])
    for idx, wt in enumerate(water_types):
        if wt.get("locked") != False:
            issues.append(f"water_type {idx} has locked={wt.get('locked')}, expected false")
        if "premium" in wt:
            issues.append(f"water_type {idx} has 'premium' field (should be removed)")
    
    # Check parameters all have locked:false
    parameters = data.get("parameters", [])
    for idx, param in enumerate(parameters):
        if param.get("locked") != False:
            issues.append(f"parameter {idx} has locked={param.get('locked')}, expected false")
        if "premium" in param:
            issues.append(f"parameter {idx} has 'premium' field (should be removed)")
    
    if issues:
        log_fail(f"GET {path}", " | ".join(issues))
    else:
        log_pass(f"GET {path}", f"{len(water_types)} water_types and {len(parameters)} parameters all unlocked")


def validate_manas(path: str, data: Dict):
    """Validate /api/manas endpoint"""
    issues = []
    
    # Check is_premium is true
    if data.get("is_premium") != True:
        issues.append(f"is_premium should be true, got {data.get('is_premium')}")
    
    # Check topics all have locked:false
    topics = data.get("topics", [])
    for idx, topic in enumerate(topics):
        if topic.get("locked") != False:
            issues.append(f"topic {idx} has locked={topic.get('locked')}, expected false")
        if "premium" in topic:
            issues.append(f"topic {idx} has 'premium' field (should be removed)")
    
    if issues:
        log_fail(f"GET {path}", " | ".join(issues))
    else:
        log_pass(f"GET {path}", f"{len(topics)} topics all unlocked")


def validate_user_no_premium(path: str, data: Dict):
    """Validate user object has no premium field"""
    user = data.get("user") or data
    if "premium" in user:
        log_fail(f"GET {path}", f"User object has 'premium' field (should be removed)")
    elif "premium_until" in user:
        log_fail(f"GET {path}", f"User object has 'premium_until' field (should be removed)")
    else:
        log_pass(f"GET {path}", "User object has no premium fields")


def validate_admin_stats(path: str, data: Dict):
    """Validate /api/admin/stats endpoint"""
    expected_fields = {"total_users", "new_registrations_7d", "ai_messages", "contact_messages", 
                      "registrations_7d", "popular_pages"}
    removed_fields = {"active_subscribers", "game_activity", "revenue", "expired_subscriptions", 
                     "pending_claims"}
    
    actual_fields = set(data.keys())
    
    issues = []
    missing = expected_fields - actual_fields
    if missing:
        issues.append(f"Missing fields: {missing}")
    
    present_removed = actual_fields & removed_fields
    if present_removed:
        issues.append(f"Removed fields still present: {present_removed}")
    
    if issues:
        log_fail(f"GET {path}", " | ".join(issues))
    else:
        log_pass(f"GET {path}", f"Has correct fields: {expected_fields}")


def main():
    print("=" * 80)
    print("DEHA VEDA BACKEND TEST SUITE - FEATURE REMOVAL VERIFICATION")
    print("=" * 80)
    print()
    
    # Step 1: Test root endpoint
    print("\n--- Testing Root Endpoint ---")
    test_surviving_endpoint("GET", "/", validation_func=validate_root)
    
    # Step 2: Test removed endpoints (no auth needed)
    print("\n--- Testing Removed Endpoints (No Auth) ---")
    test_removed_endpoint("GET", "/swara")
    test_removed_endpoint("GET", "/swara/chalisa")
    test_removed_endpoint("GET", "/games")
    test_removed_endpoint("POST", "/games/score")
    test_removed_endpoint("GET", "/games/dashboard")
    test_removed_endpoint("GET", "/plans")
    test_removed_endpoint("GET", "/membership/status")
    test_removed_endpoint("POST", "/membership/claim")
    test_removed_endpoint("GET", "/settings")
    
    # Step 3: Test surviving public endpoints
    print("\n--- Testing Surviving Public Endpoints ---")
    test_surviving_endpoint("GET", "/stats/community", validation_func=validate_community_stats)
    test_surviving_endpoint("GET", "/foods", validation_func=validate_foods)
    test_surviving_endpoint("GET", "/jala", validation_func=validate_jala)
    test_surviving_endpoint("GET", "/manas", validation_func=validate_manas)
    
    # Step 4: Test contact endpoint
    print("\n--- Testing Contact Endpoint ---")
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message for backend verification."
    }
    test_surviving_endpoint("POST", "/contact", data=contact_data)
    
    # Step 5: Test auth - register new user
    print("\n--- Testing Auth Endpoints ---")
    test_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    register_data = {
        "name": "Test User",
        "email": test_email,
        "password": "TestPassword123!"
    }
    register_response = test_surviving_endpoint("POST", "/auth/register", data=register_data, 
                                               validation_func=validate_user_no_premium)
    
    user_token = None
    if register_response:
        user_token = register_response.get("token")
        if user_token:
            log_pass("User registration", "Got access token")
        else:
            log_fail("User registration", "No token in response")
    
    # Step 6: Test /auth/me with user token
    if user_token:
        test_surviving_endpoint("GET", "/auth/me", token=user_token, 
                               validation_func=validate_user_no_premium)
    
    # Step 7: Login as admin
    print("\n--- Testing Admin Login ---")
    admin_login_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    admin_response = test_surviving_endpoint("POST", "/auth/login", data=admin_login_data)
    
    admin_token = None
    if admin_response:
        admin_token = admin_response.get("token")
        if admin_token:
            log_pass("Admin login", "Got access token")
        else:
            log_fail("Admin login", "No token in response")
    
    # Step 8: Test admin endpoints with admin token
    if admin_token:
        print("\n--- Testing Admin Endpoints ---")
        test_surviving_endpoint("GET", "/admin/stats", token=admin_token, 
                               validation_func=validate_admin_stats)
        test_surviving_endpoint("GET", "/admin/users", token=admin_token)
        
        # Test removed admin endpoints
        print("\n--- Testing Removed Admin Endpoints ---")
        test_removed_endpoint("GET", "/admin/settings", token=admin_token)
        test_removed_endpoint("GET", "/admin/claims", token=admin_token)
        test_removed_endpoint("PUT", "/admin/plans/test-code", token=admin_token, 
                            data={"price": 100})
    else:
        log_fail("Admin endpoints", "Could not test - admin login failed")
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"✅ PASSED: {len(test_results['passed'])}")
    print(f"❌ FAILED: {len(test_results['failed'])}")
    print(f"⚠️  WARNINGS: {len(test_results['warnings'])}")
    
    if test_results['failed']:
        print("\n--- FAILED TESTS ---")
        for failure in test_results['failed']:
            print(f"  • {failure['test']}: {failure['details']}")
    
    if test_results['warnings']:
        print("\n--- WARNINGS ---")
        for warning in test_results['warnings']:
            print(f"  • {warning['test']}: {warning['details']}")
    
    print("\n" + "=" * 80)
    
    # Return exit code
    return 0 if len(test_results['failed']) == 0 else 1


if __name__ == "__main__":
    exit(main())
