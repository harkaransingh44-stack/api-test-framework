"""Shared fixtures for the Restful Booker test suite."""

from __future__ import annotations

import copy
import os
from typing import Any

import pytest

from api_client import DEFAULT_BASE_URL, BookingClient
from tests.helpers import load_bookings


@pytest.fixture(scope="session")
def base_url() -> str:
    """API host. Override with the BOOKER_BASE_URL environment variable."""
    return os.getenv("BOOKER_BASE_URL", DEFAULT_BASE_URL)


@pytest.fixture(scope="session")
def client(base_url: str) -> BookingClient:
    """One HTTP client (and connection pool) shared by the whole run."""
    return BookingClient(base_url=base_url)


@pytest.fixture(scope="session")
def auth_token(client: BookingClient) -> str:
    """Fetch a token once per session using Restful Booker's public demo login.

    These are the documented demo credentials, not secrets. They can be
    overridden with BOOKER_USERNAME / BOOKER_PASSWORD.
    """
    response = client.create_token(
        os.getenv("BOOKER_USERNAME", "admin"),
        os.getenv("BOOKER_PASSWORD", "password123"),
    )
    response.raise_for_status()
    token = response.json().get("token")
    if not token:
        pytest.fail(f"Auth did not return a token: {response.text}")
    return token


@pytest.fixture
def booking_payload() -> dict[str, Any]:
    """A fresh copy of the first valid payload, safe for a test to modify."""
    return copy.deepcopy(load_bookings()["valid"][0]["payload"])


@pytest.fixture
def created_booking(
    client: BookingClient, auth_token: str, booking_payload: dict[str, Any]
):
    """Create a booking for the test, then delete it afterwards.

    Yields a dict: {"id": <bookingid>, "payload": <what was sent>}.
    Cleanup ignores 404/405 so a test that already deleted it still passes.
    """
    response = client.create_booking(booking_payload)
    response.raise_for_status()
    booking_id = response.json()["bookingid"]

    yield {"id": booking_id, "payload": booking_payload}

    client.delete_booking(booking_id, auth_token)
