# api-test-framework

[![tests](https://github.com/harkaransingh44-stack/api-test-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/harkaransingh44-stack/api-test-framework/actions/workflows/tests.yml)

A Python test framework for a public REST API and a small Playwright UI suite against a public demo store. No API key is required.

The API tests target [Restful Booker](https://restful-booker.herokuapp.com). The UI tests target [Sauce Demo](https://www.saucedemo.com/). Both are public teaching sites.

## What this covers

- A thin `requests` client for bookings: health check, auth token, create, read, update, partial update, delete
- Shared fixtures: a session-scoped client, environment-based config, an auth token, and a booking that is deleted after the test
- Data-driven cases from `data/bookings.json` (valid payloads and edge cases)
- JSON Schema checks for booking responses (required fields, types, `YYYY-MM-DD` dates)
- A small Playwright (Python) UI suite with page objects: login, add-to-cart, checkout
- `smoke`, `regression`, `api`, and `ui` markers
- GitHub Actions: lint + API tests, and a separate job for Playwright after installing Chromium. JUnit and HTML reports are uploaded as artifacts.

## Quick start

```bash
git clone https://github.com/harkaransingh44-stack/api-test-framework.git
cd api-test-framework
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest -m "not ui"                                  # API suite (needs network)
```

Requires Python 3.11 or newer.

To run the UI tests as well:

```bash
playwright install chromium
pytest -m ui
```

If Chromium is not installed, the UI tests are skipped and the rest of the suite still passes.

## Running tests

| Command | What it does |
|---------|--------------|
| `pytest` | Full suite. UI tests are skipped when Chromium is missing. Writes `reports/junit.xml` and `reports/report.html` |
| `pytest -m "not ui"` | API tests only |
| `pytest -m smoke` | Fast, high-value checks (API and UI) |
| `pytest -m regression` | Broader negative and edge-case checks |
| `pytest -m ui` | Playwright UI tests only |
| `ruff check . && ruff format --check .` | Lint and format check (same as CI) |

## Project layout

```
.
├── .github/workflows/tests.yml   # CI: lint + API job + UI job
├── data/bookings.json            # Valid and edge-case payloads
├── src/api_client/
│   └── booking_client.py         # HTTP wrapper only — no assertions
├── tests/
│   ├── conftest.py               # Fixtures, reports dir, UI skip hook
│   ├── helpers.py                # Data loader and schema assertion helper
│   ├── schemas.py                # JSON Schemas for booking responses
│   ├── test_booking_read.py      # GET ping, list, by id, filters, 404
│   ├── test_booking_write.py     # POST (data-driven), PUT, PATCH, DELETE
│   ├── test_booking_auth.py      # Token flow and forbidden requests
│   └── ui/                       # Playwright page objects and tests
├── pytest.ini
├── requirements.txt
└── requirements-dev.txt          # Adds ruff
```

## Design notes

- **Client vs tests.** `BookingClient` only builds requests and returns the raw `requests.Response`. Every assertion lives in `tests/`, so a failure always points to a test, not to hidden logic in the client.
- **Test isolation.** Tests that change data use the `created_booking` fixture, which creates a fresh booking and deletes it afterwards. Tests never depend on bookings someone else made on the shared public host.
- **Data-driven.** Adding a payload to `data/bookings.json` adds a test case without touching test code.
- **Schema validation.** Response shape is checked with `jsonschema` so type and required-field regressions are obvious.
- **Known API quirks.** Restful Booker is a teaching API with deliberate oddities. A successful DELETE returns `201`, bad credentials return `200` with `{"reason": "Bad credentials"}`, a create request missing a required field returns `500`, and invalid dates or a negative price are accepted. The edge-case tests document this actual behaviour.
- **UI selectors.** Sauce Demo exposes `data-test` attributes. The page objects use those rather than CSS classes or XPath, so the tests stay stable if the styling changes.

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `BOOKER_BASE_URL` | `https://restful-booker.herokuapp.com` | Point the API suite at another host |
| `BOOKER_USERNAME` | `admin` | Login for `POST /auth` |
| `BOOKER_PASSWORD` | `password123` | Login for `POST /auth` |
| `SAUCE_DEMO_URL` | `https://www.saucedemo.com/` | Point the UI suite at another host |
| `SAUCE_USERNAME` | `standard_user` | Sauce Demo login |
| `SAUCE_PASSWORD` | `secret_sauce` | Sauce Demo login |

The defaults are the sites' publicly documented demo credentials. No real secrets are stored in this repo.

## CI

On every push and pull request to `main`, [GitHub Actions](.github/workflows/tests.yml) runs two jobs:

1. **API tests** — Python 3.12, `ruff`, then `pytest -m "not ui"`
2. **UI tests** — install Playwright Chromium, then `pytest -m ui`

Both jobs upload `junit.xml` and `report.html` as artifacts, even when tests fail.

The API job depends on Restful Booker being up. The UI job depends on Sauce Demo being up. Either site can be temporarily slow or unavailable.

## Author

**Harkaran Singh**
LinkedIn: [linkedin.com/in/harkaran-singh784](https://www.linkedin.com/in/harkaran-singh784/)

## License

MIT. See [LICENSE](LICENSE).
