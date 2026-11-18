"""Test-side helpers (kept out of conftest so test modules can import them)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "bookings.json"


def load_bookings() -> dict[str, list[dict[str, Any]]]:
    """Read data/bookings.json. Used by fixtures and by @pytest.mark.parametrize."""
    with DATA_FILE.open(encoding="utf-8") as fh:
        return json.load(fh)


def assert_valid_schema(instance: Any, schema: dict) -> None:
    """Fail with a readable message if *instance* does not match *schema*."""
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if not errors:
        return
    lines = [
        f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}"
        for err in errors
    ]
    raise AssertionError("JSON Schema validation failed:\n" + "\n".join(lines))
