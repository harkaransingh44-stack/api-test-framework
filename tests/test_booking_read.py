"""Read-only checks: GET /ping, GET /booking and GET /booking/{id}."""

from __future__ import annotations

import pytest

from tests.helpers import assert_valid_schema
from tests.schemas import BOOKING_ID_LIST_SCHEMA, BOOKING_SCHEMA


@pytest.mark.smoke
@pytest.mark.api
def test_ping_returns_201(client):
    """GET /ping is the health check. Restful Booker returns 201 when it is up."""
    assert client.ping().status_code == 201


@pytest.mark.smoke
@pytest.mark.api
def test_list_bookings_returns_ids(client):
    """GET /booking returns a non-empty list of integer IDs."""
    response = client.get_booking_ids()

    assert response.status_code == 200
    bookings = response.json()
    assert_valid_schema(bookings, BOOKING_ID_LIST_SCHEMA)
    assert bookings, "expected at least one booking on the public host"


@pytest.mark.smoke
@pytest.mark.api
def test_get_booking_by_id_matches_created(client, created_booking):
    """GET /booking/{id} returns the fields that were sent at create time."""
    response = client.get_booking(created_booking["id"])
    payload = created_booking["payload"]

    assert response.status_code == 200
    body = response.json()
    for field in ("firstname", "lastname", "totalprice", "depositpaid"):
        assert body[field] == payload[field], f"{field} mismatch"
    assert body["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
    assert body["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]


@pytest.mark.smoke
@pytest.mark.api
def test_get_booking_has_expected_shape(client, created_booking):
    """The booking body matches the JSON Schema (types, required keys, date format)."""
    response = client.get_booking(created_booking["id"])

    assert response.status_code == 200
    assert_valid_schema(response.json(), BOOKING_SCHEMA)


@pytest.mark.regression
@pytest.mark.api
def test_get_unknown_booking_returns_404(client):
    """Asking for an ID that does not exist returns 404."""
    assert client.get_booking(999_999_999).status_code == 404


@pytest.mark.regression
@pytest.mark.api
def test_filter_bookings_by_name(client, created_booking):
    """GET /booking?firstname=&lastname= includes the booking just created."""
    payload = created_booking["payload"]

    response = client.get_booking_ids(
        firstname=payload["firstname"], lastname=payload["lastname"]
    )

    assert response.status_code == 200
    ids = [item["bookingid"] for item in response.json()]
    assert created_booking["id"] in ids
