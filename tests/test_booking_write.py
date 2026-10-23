"""Write checks: POST, PUT, PATCH and DELETE /booking."""

import pytest

from tests.helpers import load_bookings

VALID = load_bookings()["valid"]
EDGE_CASES = load_bookings()["edge_cases"]


@pytest.mark.smoke
@pytest.mark.parametrize("case", VALID, ids=[c["id"] for c in VALID])
def test_create_booking_echoes_payload(client, auth_token, case):
    """WORKED EXAMPLE - data-driven create from data/bookings.json.

    POST each valid payload, check the API echoes it back, then clean up.
    """
    payload = case["payload"]

    response = client.create_booking(payload)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["bookingid"], int)
    # Compare only the fields we sent; the API may add or drop optional ones.
    for field, expected in payload.items():
        assert body["booking"][field] == expected, f"{field} mismatch"

    client.delete_booking(body["bookingid"], auth_token)


@pytest.mark.regression
@pytest.mark.skip(reason="TODO: write this test")
@pytest.mark.parametrize("case", EDGE_CASES, ids=[c["id"] for c in EDGE_CASES])
def test_create_booking_edge_cases(client, auth_token, case):
    """TODO - data-driven negative / edge-case create.

    First run each payload by hand and note what the API really returns.
    Restful Booker is a teaching API with known bugs; for example, a missing
    required field returns 500 instead of 400. Decide per case:
    - assert the actual behaviour, or
    - mark it with pytest.mark.xfail(reason="...") and explain the expected
      behaviour - that's a good thing to talk about in an interview.
    Delete anything that did get created.
    """


@pytest.mark.skip(reason="TODO: write this test")
def test_full_update_with_token(client, auth_token, created_booking):
    """TODO - PUT /booking/{id} replaces the booking.

    Copy created_booking["payload"], change firstname and totalprice,
    then call client.update_booking(id, new_payload, auth_token).
    Assert:
    - status code is 200
    - the response body has the new values
    - a follow-up GET returns the new values too
    """


@pytest.mark.skip(reason="TODO: write this test")
def test_partial_update_with_token(client, auth_token, created_booking):
    """TODO - PATCH /booking/{id} changes only the fields you send.

    Send {"additionalneeds": "Dinner"} with client.partial_update_booking.
    Assert:
    - status code is 200
    - additionalneeds is "Dinner"
    - firstname / lastname are unchanged
    """


@pytest.mark.skip(reason="TODO: write this test")
def test_delete_booking_with_token(client, auth_token, created_booking):
    """TODO - DELETE /booking/{id} removes it.

    Assert:
    - delete returns 201 (yes, 201 - a known quirk of this API)
    - a follow-up GET /booking/{id} returns 404
    """
