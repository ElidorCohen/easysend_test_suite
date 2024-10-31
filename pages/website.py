from pages.base_page import BasePage
from pages.login_page import LoginPage


class Website(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def goto_login(self):
        login_page = LoginPage(self.page)
        login_page.goto()
        return login_page
