"""Sauce Demo login page."""

from __future__ import annotations

from playwright.sync_api import Page, expect

DEFAULT_URL = "https://www.saucedemo.com/"


class LoginPage:
    def __init__(self, page: Page, base_url: str = DEFAULT_URL) -> None:
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        expect(self.page.locator('[data-test="login-button"]')).to_be_visible()

    def login(self, username: str, password: str) -> None:
        self.page.locator('[data-test="username"]').fill(username)
        self.page.locator('[data-test="password"]').fill(password)
        self.page.locator('[data-test="login-button"]').click()

    def error_message(self) -> str:
        return self.page.locator('[data-test="error"]').inner_text()
