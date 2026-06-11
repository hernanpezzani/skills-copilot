from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_signup_for_activity_rejects_duplicate_email():
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]
    original_participants = activities[activity_name]["participants"][:]

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}
    assert activities[activity_name]["participants"] == original_participants


def test_signup_for_activity_allows_new_email():
    activity_name = "Chess Club"
    new_email = "new-student@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
    assert new_email in activities[activity_name]["participants"]

    activities[activity_name]["participants"] = original_participants
