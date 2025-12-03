from fastapi.testclient import TestClient
import urllib.parse

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic expectations: activities dict and known keys
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_user@example.com"

    # Ensure the test email is not present initially
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    signup_url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    resp = client.post(signup_url)
    assert resp.status_code == 200
    body = resp.json()
    assert "Signed up" in body.get("message", "")

    # Activity should now include the email
    assert email in activities[activity]["participants"]

    # Signing up again should fail with 400
    resp2 = client.post(signup_url)
    assert resp2.status_code == 400

    # Unregister
    unregister_url = f"/activities/{urllib.parse.quote(activity)}/unregister?email={urllib.parse.quote(email)}"
    resp3 = client.delete(unregister_url)
    assert resp3.status_code == 200
    body3 = resp3.json()
    assert "Unregistered" in body3.get("message", "")

    # Email should be removed
    assert email not in activities[activity]["participants"]
