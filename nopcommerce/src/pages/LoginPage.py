from playwright.sync_api import Locator
from nopcommerce.src.pages.ProductListPage import ProductListPage

class LoginPage:
    def __init__(self, page):
        self.page = page
        self._username_locator = page.locator("[data-test=\"username\"]")
        self._password_locator = page.locator("[data-test=\"password\"]")
        self._login_button_locator = page.locator("//input[@id='login-button']")
        self._error_message_locator = page.locator("//h3[@data-test='error']")

    def enter_username(self, u_name):
        self._username_locator.fill(u_name)

    def enter_password(self, p_word):
        self._password_locator.fill(p_word)

    def click_login(self):
        self._login_button_locator.click()

    def do_login(self, credentials):
        self.enter_username(credentials['username'])
        self.enter_password(credentials['password'])
        self.click_login()
        return ProductListPage(self.page)

    def get_error_message(self):
        return self._error_message_locator.text_content()

    @property
    def login_button(self):
        return self._login_button_locator

    @property
    def test(self):
        return self._login_button_locator

    def get_error_message_locator(self):
        return self._error_message_locator
