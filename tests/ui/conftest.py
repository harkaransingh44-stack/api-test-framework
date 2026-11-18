"""Playwright fixtures for the Sauce Demo UI suite."""

from __future__ import annotations

import os

import pytest
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

SAUCE_URL = os.getenv("SAUCE_DEMO_URL", "https://www.saucedemo.com/")
# Documented demo credentials from https://www.saucedemo.com — not secrets.
STANDARD_USER = os.getenv("SAUCE_USERNAME", "standard_user")
STANDARD_PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")


@pytest.fixture(scope="session")
def playwright_session() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_session: Playwright) -> Browser:
    browser = playwright_session.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    context = browser.new_context()
    page = context.new_page()
    page.set_default_timeout(15_000)
    yield page
    context.close()


@pytest.fixture
def sauce_url() -> str:
    return SAUCE_URL.rstrip("/") + "/"


@pytest.fixture
def standard_user() -> tuple[str, str]:
    return STANDARD_USER, STANDARD_PASSWORD
