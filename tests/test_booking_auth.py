"""Auth checks: POST /auth and token-protected endpoints."""

import pytest


@pytest.mark.smoke
def test_auth_with_valid_credentials_returns_token(client):
    """WORKED EXAMPLE - POST /auth with the demo login returns a token."""
    response = client.create_token("admin", "password123")

    assert response.status_code == 200
    token = response.json().get("token")
    assert isinstance(token, str)
    assert token, "token should not be empty"


@pytest.mark.skip(reason="TODO: write this test")
def test_auth_with_bad_password_returns_no_token(client):
    """TODO - wrong password.

    Note: this API returns 200 with {"reason": "Bad credentials"} rather
    than 401. Assert:
    - there is no "token" key in the body
    - body["reason"] == "Bad credentials"
    """


@pytest.mark.skip(reason="TODO: write this test")
def test_update_without_token_is_forbidden(client, created_booking):
    """TODO - PUT with no token.

    Call client.update_booking(id, payload, token=None).
    Assert:
    - status code is 403
    - a follow-up GET shows the booking is unchanged
    """


@pytest.mark.skip(reason="TODO: write this test")
def test_delete_with_invalid_token_is_forbidden(client, created_booking):
    """TODO - DELETE with a made-up token.

    Call client.delete_booking(id, token="not-a-real-token").
    Assert:
    - status code is 403
    - the booking still exists (GET returns 200)
    """
