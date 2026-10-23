"""Thin HTTP client for the public Restful Booker API."""

from api_client.booking_client import DEFAULT_BASE_URL, BookingClient

__all__ = ["BookingClient", "DEFAULT_BASE_URL"]
