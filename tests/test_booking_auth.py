"""Auth checks: POST /auth and token-protected endpoints."""

from __future__ import annotations

import os

import pytest


@pytest.mark.smoke
@pytest.mark.api
def test_auth_with_valid_credentials_returns_token(client):
    """POST /auth with the demo login returns a non-empty token."""
    response = client.create_token(
        os.getenv("BOOKER_USERNAME", "admin"),
        os.getenv("BOOKER_PASSWORD", "password123"),
    )

    assert response.status_code == 200
    token = response.json().get("token")
    assert isinstance(token, str)
    assert token, "token should not be empty"


@pytest.mark.regression
@pytest.mark.api
def test_auth_with_bad_password_returns_no_token(client):
    """Wrong password: this API returns 200 with a reason, not 401."""
    response = client.create_token("admin", "this-is-not-the-password")

    assert response.status_code == 200
    body = response.json()
    assert "token" not in body
    assert body["reason"] == "Bad credentials"


@pytest.mark.regression
@pytest.mark.api
def test_update_without_token_is_forbidden(client, created_booking):
    """PUT with no token is rejected and the booking is left unchanged."""
    booking_id = created_booking["id"]
    original = created_booking["payload"]
    attempted = {**original, "firstname": "ShouldNotStick"}

    response = client.update_booking(booking_id, attempted, token=None)

    assert response.status_code == 403

    follow_up = client.get_booking(booking_id)
    assert follow_up.status_code == 200
    assert follow_up.json()["firstname"] == original["firstname"]


@pytest.mark.regression
@pytest.mark.api
def test_delete_with_invalid_token_is_forbidden(client, created_booking):
    """DELETE with a made-up token is rejected and the booking still exists."""
    booking_id = created_booking["id"]

    response = client.delete_booking(booking_id, token="not-a-real-token")

    assert response.status_code == 403
    assert client.get_booking(booking_id).status_code == 200
