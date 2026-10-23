"""Test-side helpers (kept out of conftest so test modules can import them)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "bookings.json"


def load_bookings() -> dict[str, list[dict[str, Any]]]:
    """Read data/bookings.json. Used by fixtures and by @pytest.mark.parametrize."""
    with DATA_FILE.open(encoding="utf-8") as fh:
        return json.load(fh)
