"""Thin wrapper around the Restful Booker REST API.

This module is plumbing only: it builds URLs, sets headers and returns the raw
``requests.Response``. It never asserts anything. All checks live in ``tests/``.

API docs: https://restful-booker.herokuapp.com/apidoc/index.html
"""

from __future__ import annotations

from typing import Any

import requests

DEFAULT_BASE_URL = "https://restful-booker.herokuapp.com"
DEFAULT_TIMEOUT = 15  # seconds; the public host can be slow to wake up


class BookingClient:
    """Small client for the /auth and /booking endpoints."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self.session.headers.update(
            {"Accept": "application/json", "Content-Type": "application/json"}
        )

    # ------------------------------------------------------------------ helpers
    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    @staticmethod
    def _auth_headers(token: str | None) -> dict[str, str]:
        # Restful Booker expects the token as a cookie named "token".
        return {"Cookie": f"token={token}"} if token else {}

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, self._url(path), **kwargs)

    # --------------------------------------------------------------------- auth
    def ping(self) -> requests.Response:
        """GET /ping - health check (returns 201 when the API is up)."""
        return self._request("GET", "/ping")

    def create_token(self, username: str, password: str) -> requests.Response:
        """POST /auth - returns {"token": "..."} on success."""
        return self._request(
            "POST", "/auth", json={"username": username, "password": password}
        )

    # ------------------------------------------------------------------- read
    def get_booking_ids(self, **filters: str) -> requests.Response:
        """GET /booking - list of {"bookingid": n}. Optional query filters:
        firstname, lastname, checkin, checkout."""
        return self._request("GET", "/booking", params=filters or None)

    def get_booking(self, booking_id: int) -> requests.Response:
        """GET /booking/{id} - one booking as JSON (404 if it does not exist)."""
        return self._request("GET", f"/booking/{booking_id}")

    # ------------------------------------------------------------------ write
    def create_booking(self, payload: dict[str, Any]) -> requests.Response:
        """POST /booking - returns {"bookingid": n, "booking": {...}}."""
        return self._request("POST", "/booking", json=payload)

    def update_booking(
        self, booking_id: int, payload: dict[str, Any], token: str | None
    ) -> requests.Response:
        """PUT /booking/{id} - full replace. Needs a token."""
        return self._request(
            "PUT",
            f"/booking/{booking_id}",
            json=payload,
            headers=self._auth_headers(token),
        )

    def partial_update_booking(
        self, booking_id: int, fields: dict[str, Any], token: str | None
    ) -> requests.Response:
        """PATCH /booking/{id} - update only the given fields. Needs a token."""
        return self._request(
            "PATCH",
            f"/booking/{booking_id}",
            json=fields,
            headers=self._auth_headers(token),
        )

    def delete_booking(self, booking_id: int, token: str | None) -> requests.Response:
        """DELETE /booking/{id} - returns 201 on success. Needs a token."""
        return self._request(
            "DELETE", f"/booking/{booking_id}", headers=self._auth_headers(token)
        )
