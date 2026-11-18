"""Login checks against the public Sauce Demo store."""

from __future__ import annotations

import pytest

from tests.ui.pages.inventory_page import InventoryPage
from tests.ui.pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login_shows_inventory(page, sauce_url, standard_user):
    username, password = standard_user
    login = LoginPage(page, sauce_url)

    login.open()
    login.login(username, password)

    InventoryPage(page).wait_until_loaded()
    assert "inventory" in page.url


@pytest.mark.ui
@pytest.mark.regression
def test_locked_out_user_sees_error(page, sauce_url, standard_user):
    _, password = standard_user
    login = LoginPage(page, sauce_url)

    login.open()
    login.login("locked_out_user", password)

    message = login.error_message()
    assert "locked out" in message.lower()
    assert "inventory" not in page.url
