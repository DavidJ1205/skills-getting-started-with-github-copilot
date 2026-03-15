"""Tests for the Mergington High School API using FastAPI TestClient."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


class TestActivities:
    """Test suite for /activities endpoints."""

    def test_get_activities_returns_dict_with_known_keys(self):
        """Arrange-Act-Assert: GET /activities returns dict with known keys."""
        # Arrange: Define expected activity keys
        expected_activity_keys = [
            "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
            "Basketball Club", "Art Club", "Drama Society", "Math Olympiad", "Science Club"
        ]

        # Act: Make GET request to /activities
        response = client.get("/activities")

        # Assert: Check response status and structure
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert set(activities.keys()) == set(expected_activity_keys)

        # Assert each activity has required fields
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignup:
    """Test suite for signup endpoints."""

    def test_post_signup_new_email_successfully(self):
        """Arrange-Act-Assert: POST /activities/{activity}/signup signs up new email successfully."""
        # Arrange: Prepare test data
        activity_name = "Chess Club"
        test_email = "newstudent@mergington.edu"

        # Act: Make POST request to sign up
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Assert: Check response status and message
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert test_email in data["message"]
        assert activity_name in data["message"]

    def test_post_signup_duplicate_email_returns_400(self):
        """Arrange-Act-Assert: POST same email twice returns 400 error."""
        # Arrange: Use existing participant from Chess Club
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"

        # Act: Try to sign up with same email twice
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # Assert: Check for 400 status code
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()


class TestUnregister:
    """Test suite for unregister endpoint."""

    def test_delete_signup_removes_email_successfully(self):
        """Arrange-Act-Assert: DELETE /activities/{activity}/signup removes email and returns success."""
        # Arrange: Sign up first, then delete
        activity_name = "Programming Class"
        test_email = "deletetest@mergington.edu"

        # First sign up the test email
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Act: Make DELETE request
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Assert: Check response status and message
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Removed" in data["message"]
        assert test_email in data["message"]
        assert activity_name in data["message"]

    def test_delete_nonexistent_email_returns_404(self):
        """Arrange-Act-Assert: DELETE non-existent email returns 404."""
        # Arrange: Use email not signed up
        activity_name = "Chess Club"
        nonexistent_email = "nonexistent@mergington.edu"

        # Act: Make DELETE request
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": nonexistent_email}
        )

        # Assert: Check for 404 status code
        assert response.status_code == 404

    def test_delete_from_nonexistent_activity_returns_404(self):
        """Arrange-Act-Assert: DELETE from non-existent activity returns 404."""
        # Arrange: Use non-existent activity
        nonexistent_activity = "Nonexistent Activity"
        test_email = "test@mergington.edu"

        # Act: Make DELETE request
        response = client.delete(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": test_email}
        )

        # Assert: Check for 404 status code
        assert response.status_code == 404