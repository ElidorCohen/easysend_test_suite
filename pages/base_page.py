class BasePage:
    def __init__(self, page):
        self.page = page

    def go_to(self, url):
        self.page.goto(url)
