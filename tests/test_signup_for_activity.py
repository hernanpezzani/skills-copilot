import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities_state():
    snapshot = {name: details["participants"][:] for name, details in activities.items()}
    yield
    for name, participants in snapshot.items():
        activities[name]["participants"] = participants


def test_signup_for_activity_rejects_duplicate_email():
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}
    assert existing_email in activities[activity_name]["participants"]


def test_signup_for_activity_allows_new_email():
    activity_name = "Chess Club"
    new_email = "new-student@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
    assert new_email in activities[activity_name]["participants"]
