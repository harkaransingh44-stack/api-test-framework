"""JSON Schemas for Restful Booker responses.

Kept in the test package, not in the client, so the client stays assertion-free.
"""

from __future__ import annotations

DATE_PATTERN = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"

BOOKING_DATES_SCHEMA: dict = {
    "type": "object",
    "required": ["checkin", "checkout"],
    "properties": {
        "checkin": {"type": "string", "pattern": DATE_PATTERN},
        "checkout": {"type": "string", "pattern": DATE_PATTERN},
    },
    "additionalProperties": False,
}

BOOKING_SCHEMA: dict = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "integer"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": BOOKING_DATES_SCHEMA,
        "additionalneeds": {"type": "string"},
    },
}

CREATED_BOOKING_SCHEMA: dict = {
    "type": "object",
    "required": ["bookingid", "booking"],
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING_SCHEMA,
    },
}

BOOKING_ID_LIST_SCHEMA: dict = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["bookingid"],
        "properties": {"bookingid": {"type": "integer"}},
        "additionalProperties": True,
    },
}
