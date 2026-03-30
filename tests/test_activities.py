from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# GET /activities
# ---------------------------------------------------------------------------

class TestGetActivities:
    def test_returns_200(self, client: TestClient):
        response = client.get("/activities")
        assert response.status_code == 200

    def test_returns_dict_with_known_activities(self, client: TestClient):
        data = client.get("/activities").json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Science Olympiad" in data

    def test_activity_has_required_fields(self, client: TestClient):
        data = client.get("/activities").json()
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

class TestSignup:
    def test_signup_success(self, client: TestClient):
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"},
        )
        assert response.status_code == 200
        assert "newstudent@mergington.edu" in response.json()["message"]

    def test_signup_adds_participant(self, client: TestClient):
        email = "newstudent@mergington.edu"
        client.post("/activities/Chess Club/signup", params={"email": email})
        activities = client.get("/activities").json()
        assert email in activities["Chess Club"]["participants"]

    def test_signup_unknown_activity_returns_404(self, client: TestClient):
        response = client.post(
            "/activities/Nonexistent Club/signup",
            params={"email": "student@mergington.edu"},
        )
        assert response.status_code == 404

    def test_signup_duplicate_email_returns_400(self, client: TestClient):
        email = "michael@mergington.edu"  # already seeded in Chess Club
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email},
        )
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/participants
# ---------------------------------------------------------------------------

class TestUnregister:
    def test_unregister_success(self, client: TestClient):
        email = "michael@mergington.edu"  # seeded in Chess Club
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": email},
        )
        assert response.status_code == 200
        assert email in response.json()["message"]

    def test_unregister_removes_participant(self, client: TestClient):
        email = "michael@mergington.edu"
        client.delete("/activities/Chess Club/participants", params={"email": email})
        activities = client.get("/activities").json()
        assert email not in activities["Chess Club"]["participants"]

    def test_unregister_unknown_activity_returns_404(self, client: TestClient):
        response = client.delete(
            "/activities/Nonexistent Club/participants",
            params={"email": "student@mergington.edu"},
        )
        assert response.status_code == 404

    def test_unregister_email_not_in_activity_returns_404(self, client: TestClient):
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "notamember@mergington.edu"},
        )
        assert response.status_code == 404
