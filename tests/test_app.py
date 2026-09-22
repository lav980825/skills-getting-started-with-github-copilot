from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activities():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Soccer Club": {
                "description": "Practice soccer skills and compete in friendly matches",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
                "max_participants": 22,
                "participants": [],
            },
        }
    )


def test_get_activities_returns_activity_data():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_participant_to_activity():
    # Arrange
    reset_activities()
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Soccer Club/signup?email=" + email)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Soccer Club"
    assert email in activities["Soccer Club"]["participants"]


def test_signup_rejects_duplicate_registration():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup?email=" + email)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_removes_participant_from_activity():
    # Arrange
    reset_activities()
    email = "michael@mergington.edu"

    # Act
    response = client.delete("/activities/Chess Club/participants?email=" + email)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_unknown_activity_returns_404_for_signup():
    # Arrange
    reset_activities()

    # Act
    response = client.post("/activities/Unknown Club/signup?email=test@example.com")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
