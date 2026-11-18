"""Sauce Demo inventory and cart pages."""

from __future__ import annotations

from playwright.sync_api import Page, expect


class InventoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def wait_until_loaded(self) -> None:
        expect(self.page.locator('[data-test="inventory-container"]')).to_be_visible()

    def add_item(self, item_slug: str) -> None:
        self.page.locator(f'[data-test="add-to-cart-{item_slug}"]').click()

    def cart_badge_count(self) -> int:
        badge = self.page.locator('[data-test="shopping-cart-badge"]')
        expect(badge).to_be_visible()
        return int(badge.inner_text())

    def open_cart(self) -> None:
        self.page.locator('[data-test="shopping-cart-link"]').click()


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def wait_until_loaded(self) -> None:
        expect(
            self.page.locator('[data-test="cart-contents-container"]')
        ).to_be_visible()

    def item_names(self) -> list[str]:
        return self.page.locator('[data-test="inventory-item-name"]').all_inner_texts()

    def checkout(self) -> None:
        self.page.locator('[data-test="checkout"]').click()


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def fill_info(self, first: str, last: str, postal: str) -> None:
        self.page.locator('[data-test="firstName"]').fill(first)
        self.page.locator('[data-test="lastName"]').fill(last)
        self.page.locator('[data-test="postalCode"]').fill(postal)
        self.page.locator('[data-test="continue"]').click()

    def finish(self) -> None:
        self.page.locator('[data-test="finish"]').click()

    def complete_header(self) -> str:
        header = self.page.locator('[data-test="complete-header"]')
        expect(header).to_be_visible()
        return header.inner_text()
