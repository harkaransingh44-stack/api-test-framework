"""Read-only checks: GET /booking and GET /booking/{id}."""

import pytest


@pytest.mark.smoke
def test_list_bookings_returns_ids(client):
    """WORKED EXAMPLE - GET /booking returns a non-empty list of integer IDs."""
    response = client.get_booking_ids()

    assert response.status_code == 200
    bookings = response.json()
    assert isinstance(bookings, list)
    assert bookings, "expected at least one booking on the public host"
    assert all(isinstance(item["bookingid"], int) for item in bookings)


@pytest.mark.skip(reason="TODO: write this test")
def test_get_booking_by_id_matches_created(client, created_booking):
    """TODO - GET /booking/{id} returns what was created.

    Use the ``created_booking`` fixture so the data is yours.
    Assert:
    - status code is 200
    - firstname, lastname, totalprice, depositpaid match created_booking["payload"]
    - bookingdates.checkin and bookingdates.checkout match
    """


@pytest.mark.skip(reason="TODO: write this test")
def test_get_booking_has_expected_shape(client, created_booking):
    """TODO - the response has the right keys and types.

    Assert:
    - keys include firstname, lastname, totalprice, depositpaid, bookingdates
    - totalprice is an int, depositpaid is a bool
    - bookingdates has checkin and checkout strings in YYYY-MM-DD form
    Stretch: replace this with a jsonschema check.
    """


@pytest.mark.skip(reason="TODO: write this test")
def test_get_unknown_booking_returns_404(client):
    """TODO - asking for an ID that does not exist.

    Pick an ID that will never exist (e.g. 999999999).
    Assert:
    - status code is 404
    """


@pytest.mark.skip(reason="TODO: write this test")
def test_filter_bookings_by_name(client, created_booking):
    """TODO - GET /booking?firstname=...&lastname=... finds your booking.

    Use client.get_booking_ids(firstname=..., lastname=...).
    Assert:
    - status code is 200
    - created_booking["id"] is in the returned bookingid values
    """
