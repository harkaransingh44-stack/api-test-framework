# api-test-framework

[![tests](https://github.com/harkaransingh44-stack/api-test-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/harkaransingh44-stack/api-test-framework/actions/workflows/tests.yml)

PyTest + requests test suite for the public [Restful Booker](https://restful-booker.herokuapp.com) hotel-booking API, covering CRUD, token auth, data-driven cases and CI on GitHub Actions. No API key needed.

Built by **Harkaran Singh** (SDET II) as a portfolio project for REST API testing with Python and PyTest.

> **Status:** In progress. The client, fixtures, data and CI are in place, and more test cases are being added.

---

## What this covers

- A thin `requests`-based client for bookings: auth token, create, read, update, partial update, delete
- Shared PyTest fixtures: session client, base URL from the environment, auth token, and a booking that cleans itself up
- Data-driven tests from `data/bookings.json`, with valid payloads and edge cases
- `smoke` and `regression` markers
- GitHub Actions: lint and test on every push and pull request, with JUnit and HTML reports saved as artifacts

## Quick start

```bash
git clone https://github.com/harkaransingh44-stack/api-test-framework.git
cd api-test-framework
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest
```

Requires Python 3.11 or newer.

## Running tests

| Command | What it does |
|---------|--------------|
| `pytest` | Full suite; writes `reports/junit.xml` and `reports/report.html` |
| `pytest -m smoke` | Fast, high-value checks only |
| `pytest -m regression` | Broader negative and edge-case checks |
| `pytest -k auth` | Tests whose name matches "auth" |
| `ruff check . && ruff format --check .` | Lint and format check (same as CI) |

## Project layout

```
.
├── .github/workflows/tests.yml   # CI: lint + pytest + report artifacts
├── data/bookings.json            # Valid and edge-case payloads for parametrized tests
├── src/api_client/
│   └── booking_client.py         # HTTP wrapper only - no assertions
├── tests/
│   ├── conftest.py               # Fixtures: client, base_url, auth_token, created_booking
│   ├── helpers.py                # Test data loader
│   ├── test_booking_read.py      # GET list, GET by id, filters, 404
│   ├── test_booking_write.py     # POST (data-driven), PUT, PATCH, DELETE
│   └── test_booking_auth.py      # Token flow and forbidden requests
├── pytest.ini
├── requirements.txt              # Runtime test dependencies (pinned)
└── requirements-dev.txt          # Adds ruff for linting
```

## Design notes

- **Client vs tests.** `BookingClient` only builds requests and returns the raw `requests.Response`. Every assertion lives in `tests/`, so a failure always points to a test, not to hidden logic in the client.
- **Test isolation.** Tests that change data use the `created_booking` fixture, which creates a fresh booking and deletes it afterwards, so tests never depend on bookings someone else made on the shared public host.
- **Data-driven.** Adding a new payload to `data/bookings.json` adds a new test case without touching any code.
- **Known API quirks.** Restful Booker is a teaching API with some deliberate oddities. A successful DELETE returns `201`, bad credentials return `200` with `{"reason": "Bad credentials"}`, and a create request missing a required field returns `500`. Tests document the actual behaviour.

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `BOOKER_BASE_URL` | `https://restful-booker.herokuapp.com` | Point the suite at another host, e.g. a local Docker copy |
| `BOOKER_USERNAME` | `admin` | Login for `POST /auth` |
| `BOOKER_PASSWORD` | `password123` | Login for `POST /auth` |

The defaults are Restful Booker's publicly documented demo credentials. No real secrets are stored in this repo.

## CI

On every push and pull request to `main`, [GitHub Actions](.github/workflows/tests.yml):

1. Sets up Python 3.12 and installs pinned dependencies
2. Runs `ruff check` and `ruff format --check`
3. Runs `pytest`
4. Uploads `junit.xml` and `report.html` as the `pytest-reports` artifact, even when tests fail

## Author

**Harkaran Singh**
LinkedIn: [linkedin.com/in/harkaran-singh784](https://www.linkedin.com/in/harkaran-singh784/)

## License

MIT. See [LICENSE](LICENSE).
