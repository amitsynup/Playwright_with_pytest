import time

import pytest as pytest
from playwright.sync_api import expect
from nopcommerce.src.pages.LoginPage import LoginPage
from nopcommerce.tests.conftest import set_up_tear_down

class TestLogin:

    @pytest.mark.smoke
    def test_valid_credential(self, set_up_tear_down) -> None:
        page = set_up_tear_down
        credentials = {'username': 'standard_user', 'password': 'secret_sauce'}
        login_page = LoginPage(page)
        product_page = login_page.do_login(credentials)
        expect(product_page.product_header).to_be_visible()
        expect(product_page.product_header).to_have_text("Products")

    @pytest.mark.smoke
    def test_invalid_credential(self, set_up_tear_down) -> None:
        page = set_up_tear_down
        credentials = {'username': 'standard_user13', 'password': 'secret_sauce'}
        login_page = LoginPage(page)
        login_page.do_login(credentials)
        error_message = login_page.get_error_message()
        print("testing")
        print(error_message)
        assert "Epic sadface: Username and password do not match any user in this service" in error_message

    @pytest.mark.regression
    def test_without_credential(self, set_up_tear_down) -> None:
        page = set_up_tear_down
        credentials = {'username': '', 'password': ''}
        login_page = LoginPage(page)
        login_page.do_login(credentials)
        error_message_locator = login_page.get_error_message_locator()
        expect(error_message_locator).to_have_text("Epic sadface: Username is required")

    @pytest.mark.regression
    def test_logout(self, set_up_tear_down) -> None:
        page = set_up_tear_down
        credentials = {'username': 'standard_user', 'password': 'secret_sauce'}
        login_page = LoginPage(page)
        product_page = login_page.do_login(credentials)
        product_page.do_logout()
        time.sleep(5)
        if login_page.login_button.is_visible():
            login_button_text = login_page.login_button.text_content()
            print(f"Actual login button text: {login_button_text}")
            # expect(login_button_text).to_have_text("LOGIN")
        else:
            print("Login button is not visible")
            assert False, "Login button is not visible"

    @pytest.mark.regression
    def test_access_inventory_without_login(self, set_up_tear_down):
        page = set_up_tear_down
        page.goto("https://www.saucedemo.com/inventory.html")
        login_page = LoginPage(page)
        error_message = login_page.get_error_message()
        print(error_message)
        assert "Epic sadface: You can only access '/inventory.html' when you are logged in." in error_message

