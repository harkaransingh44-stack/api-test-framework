"""Write checks: POST, PUT, PATCH and DELETE /booking."""

from __future__ import annotations

import pytest

from tests.helpers import assert_valid_schema, load_bookings
from tests.schemas import BOOKING_SCHEMA, CREATED_BOOKING_SCHEMA

VALID = load_bookings()["valid"]
EDGE_CASES = load_bookings()["edge_cases"]


@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.parametrize("case", VALID, ids=[c["id"] for c in VALID])
def test_create_booking_echoes_payload(client, auth_token, case):
    """Data-driven create from data/bookings.json. POST, echo-check, clean up."""
    payload = case["payload"]

    response = client.create_booking(payload)

    assert response.status_code == 200
    body = response.json()
    assert_valid_schema(body, CREATED_BOOKING_SCHEMA)
    for field, expected in payload.items():
        assert body["booking"][field] == expected, f"{field} mismatch"

    client.delete_booking(body["bookingid"], auth_token)


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize("case", EDGE_CASES, ids=[c["id"] for c in EDGE_CASES])
def test_create_booking_edge_cases(client, auth_token, case):
    """Data-driven negative / edge-case create.

    Restful Booker is a teaching API with known validation gaps. These tests
    assert the *actual* behaviour (documented in data/bookings.json) so a change
    in the API would fail the suite. A production booking API should reject
    invalid dates, negative prices and wrong types with 4xx, not accept them.
    """
    response = client.create_booking(case["payload"])

    assert response.status_code == case["expected_status"]

    if case.get("expect_totalprice_null"):
        assert response.json()["booking"]["totalprice"] is None

    booking_id = None
    if response.status_code == 200:
        booking_id = response.json().get("bookingid")
    if booking_id:
        client.delete_booking(booking_id, auth_token)


@pytest.mark.smoke
@pytest.mark.api
def test_full_update_with_token(client, auth_token, created_booking):
    """PUT /booking/{id} replaces the booking when a valid token is sent."""
    booking_id = created_booking["id"]
    updated = {
        **created_booking["payload"],
        "firstname": "Updated",
        "totalprice": 999,
    }

    response = client.update_booking(booking_id, updated, auth_token)

    assert response.status_code == 200
    body = response.json()
    assert_valid_schema(body, BOOKING_SCHEMA)
    assert body["firstname"] == "Updated"
    assert body["totalprice"] == 999

    follow_up = client.get_booking(booking_id)
    assert follow_up.status_code == 200
    assert follow_up.json()["firstname"] == "Updated"
    assert follow_up.json()["totalprice"] == 999


@pytest.mark.smoke
@pytest.mark.api
def test_partial_update_with_token(client, auth_token, created_booking):
    """PATCH /booking/{id} changes only the fields that were sent."""
    booking_id = created_booking["id"]
    original_name = created_booking["payload"]["firstname"]

    response = client.partial_update_booking(
        booking_id, {"additionalneeds": "Dinner"}, auth_token
    )

    assert response.status_code == 200
    body = response.json()
    assert body["additionalneeds"] == "Dinner"
    assert body["firstname"] == original_name
    assert body["lastname"] == created_booking["payload"]["lastname"]


@pytest.mark.smoke
@pytest.mark.api
def test_delete_booking_with_token(client, auth_token, created_booking):
    """DELETE /booking/{id} removes it. A successful delete returns 201 on this API."""
    booking_id = created_booking["id"]

    response = client.delete_booking(booking_id, auth_token)

    assert response.status_code == 201
    assert client.get_booking(booking_id).status_code == 404
