from pages.base_page import BasePage
from playwright.sync_api import Page
from pages.home_page import HomePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.__form_input_locator = self.page.locator("form#login input")
        self.__submit_button = self.page.get_by_role("navigation").get_by_role("button", name="Log in")
        self.username_error_locator = self.page.locator("text='Name is a required field.'")
        self.password_error_locator = self.page.locator("text='Password is a required field.'")

    def goto(self):
        self.page.locator("button:has-text('Log in')").click()

    def __fill_username(self, username):
        self.__form_input_locator.nth(0).fill(username)

    def __fill_password(self, password):
        self.__form_input_locator.nth(1).fill(password)

    def fill_credentials(self, username, password):
        self.__fill_username(username)
        self.__fill_password(password)

    def submit(self):
        self.__submit_button.click()
        return HomePage(self.page)

    def is_username_error_visible(self):
        return self.username_error_locator.is_visible()

    def is_password_error_visible(self):
        return self.password_error_locator.is_visible()

    def check_username_error(self, expected_message):
        assert self.username_error_locator.text_content() == expected_message, \
            "Expected username error message not found"

    def check_password_error(self, expected_message):
        assert self.password_error_locator.text_content() == expected_message, \
            "Expected password error message not found"

    def is_login_persistent(self):
        login_indicator = self.page.locator("button span:has-text('Hello, John')")
        return login_indicator.is_visible()

