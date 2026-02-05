import pytest
from fastapi.testclient import TestClient
import copy
from src.app import app, get_activities_store

client = TestClient(app)

# Original activities data for reset
ORIGINAL_ACTIVITIES = {
    "Soccer Team": {
        "description": "Competitive soccer training and matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": []
    },
    "Basketball Club": {
        "description": "Basketball skills development and team games",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Theater performance and acting workshops",
        "schedule": "Mondays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": []
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Math Olympiad": {
        "description": "Advanced math problem solving and competition preparation",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    app.state.activities = copy.deepcopy(ORIGINAL_ACTIVITIES)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Use a unique email for testing
    import uuid
    test_email = f"pytestuser_{uuid.uuid4()}@mergington.edu"
    activity = "Chess Club"

    # Unregister if already present (ignore error)
    client.post(f"/activities/{activity}/unregister?email={test_email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200, f"Signup failed unexpectedly: {response.status_code} {response.text}"
    assert f"Signed up {test_email}" in response.json()["message"]

    # Confirm participant is present
    activities_resp = client.get("/activities")
    assert activities_resp.status_code == 200
    activities_data = activities_resp.json()
    assert test_email in activities_data[activity]["participants"], "Participant not found after signup."

    # Try signing up again (should fail)
    response2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response2.status_code == 400

    # Unregister
    response3 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert response3.status_code == 200, f"Unregister failed: {response3.status_code} {response3.text}"
    assert f"Unregistered {test_email}" in response3.json()["message"]

    # Unregister again (should fail)
    response4 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert response4.status_code == 404
