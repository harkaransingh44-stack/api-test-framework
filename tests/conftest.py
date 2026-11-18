"""Shared fixtures and hooks for the Restful Booker and Sauce Demo suites."""

from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any

import pytest

from api_client import DEFAULT_BASE_URL, BookingClient
from tests.helpers import load_bookings


def pytest_configure(config: pytest.Config) -> None:
    Path("reports").mkdir(exist_ok=True)


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Skip Playwright tests when Chromium is not installed."""
    ui_items = [item for item in items if item.get_closest_marker("ui")]
    if not ui_items:
        return
    if _chromium_available():
        return
    skip = pytest.mark.skip(
        reason="Playwright Chromium is not installed. Run: playwright install chromium"
    )
    for item in ui_items:
        item.add_marker(skip)


def _chromium_available() -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            browser.close()
    except Exception:
        return False
    return True


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
    Cleanup ignores 404 so a test that already deleted it still passes.
    """
    response = client.create_booking(booking_payload)
    response.raise_for_status()
    booking_id = response.json()["bookingid"]

    yield {"id": booking_id, "payload": booking_payload}

    delete = client.delete_booking(booking_id, auth_token)
    if delete.status_code not in {201, 404}:
        # Don't fail the test on cleanup, but leave a breadcrumb in the report.
        print(f"cleanup: DELETE /booking/{booking_id} returned {delete.status_code}")
