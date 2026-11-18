"""Cart and checkout checks against the public Sauce Demo store."""

from __future__ import annotations

import pytest

from tests.ui.pages.inventory_page import CartPage, CheckoutPage, InventoryPage
from tests.ui.pages.login_page import LoginPage

BACKPACK = "sauce-labs-backpack"


@pytest.mark.ui
@pytest.mark.smoke
def test_add_to_cart_updates_badge_and_cart(page, sauce_url, standard_user):
    username, password = standard_user
    LoginPage(page, sauce_url).open()
    LoginPage(page, sauce_url).login(username, password)

    inventory = InventoryPage(page)
    inventory.wait_until_loaded()
    inventory.add_item(BACKPACK)

    assert inventory.cart_badge_count() == 1

    inventory.open_cart()
    cart = CartPage(page)
    cart.wait_until_loaded()
    assert any("Sauce Labs Backpack" in name for name in cart.item_names())


@pytest.mark.ui
@pytest.mark.regression
def test_checkout_completes_for_standard_user(page, sauce_url, standard_user):
    username, password = standard_user
    LoginPage(page, sauce_url).open()
    LoginPage(page, sauce_url).login(username, password)

    inventory = InventoryPage(page)
    inventory.wait_until_loaded()
    inventory.add_item(BACKPACK)
    inventory.open_cart()

    cart = CartPage(page)
    cart.wait_until_loaded()
    cart.checkout()

    checkout = CheckoutPage(page)
    checkout.fill_info("Avery", "Tester", "95757")
    checkout.finish()
    assert "thank you for your order" in checkout.complete_header().lower()
