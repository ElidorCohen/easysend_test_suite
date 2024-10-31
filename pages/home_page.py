from playwright.sync_api import expect
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.months = ["January", "February", "March", "April", "May", "June", "July",
                        "August", "September", "October", "November", "December"]
        self.month_locator = self.page.locator("span.theme__title___2Ue3-").nth(0)
        self.adults_dropdown = self.page.locator("div[data-react-toolbox='dropdown']").nth(0)
        self.children_dropdown = self.page.locator("div[data-react-toolbox='dropdown']").nth(1)
        self.load_more_button = self.page.locator("button:has-text('Load more')")
        self.slider_knob = self.page.locator("div.theme__knob____QAHG.PurpleSlider__knob___lSlRq")
        self.slider_inner = self.page.locator("div.theme__innerknob___20XNj.PurpleSlider__innerknob___2wxLd")
        self.target_price_locator = self.page.locator(
            "input[class*='theme__inputElement___27dyY theme__filled___1UI7Z']:not([name])")

    def set_departing(self, date):
        day, month, year = date.split("/")
        self.open_date_picker("departing")
        self.select_year(year)
        self.select_month(self.months[int(month) - 1])
        self.select_day(day, month, year)

    def set_returning(self, date):
        day, month, year = date.split("/")
        self.open_date_picker("returning")
        self.select_year(year)
        self.select_month(self.months[int(month) - 1])
        self.select_day(day, month, year)

    def open_date_picker(self, picker_type):
        match picker_type:
            case "departing":
                self.page.locator("input[role='input']").nth(0).click()
            case "returning":
                self.page.locator("input[role='input']").nth(1).click()

    def select_year(self, year):
        self.page.locator("span#years").click()
        self.page.locator(f"ul > li[id=\'{year}\']").click()

    def select_month(self, month):
        current_month = self.get_month()

        current_month_index = self.months.index(current_month)
        target_month_index = self.months.index(month)
        times = abs(current_month_index - target_month_index)

        direction = "left" if current_month_index > target_month_index else "right"
        match direction:
            case "left":
                for i in range(times):
                    self.page.locator("button[id='left']").click()
            case "right":
                for i in range(times):
                    self.page.locator("button[id='right']").click()

    def get_month(self):
        return self.month_locator.text_content().split()[0].strip()

    def is_valid_date(self, day, month, year):
        day = int(day)
        month = int(month)
        year = int(year)

        days_in_month = [31, 28 + (1 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 0), 31, 30, 31,
                         30, 31, 31, 30, 31, 30, 31]
        return 1 <= month <= 12 and 1 <= day <= days_in_month[month - 1]

    def select_day_for_departing_or_returning(self, day):
        self.page.locator("div.theme__day___3cb3g > span").nth(int(day) - 1).click(timeout=1000)

    def select_day(self, day, month, year):
        if not self.is_valid_date(day, month, year):
            print(f"Skipped test due to invalid day input: {day}/{month}/{year} does not exist.")
            return False
        day_index = int(day) - 1
        try:
            self.page.locator("div.theme__day___3cb3g > span").nth(day_index).click(timeout=1000)
        except TimeoutError:
            print(f"Could not click day {day} as it is not available in the calendar.")
        return True

    def submit_selection(self):
        self.page.locator(".theme__button___1iKuo.theme__flat___2ui7t.theme__neutral___uDC3j.theme__button___3HGWm.theme__button___14VKJ").nth(1).click()

    def select_adults(self, number):
        self.adults_dropdown.click()
        self.page.get_by_text(str(number), exact=True).first.click(timeout=500)

    def get_selected_adults(self, expected_value):
        return self.page.locator(
            "li.theme__selected___2Uc3r.WhiteDropDown__selected___3y0b0"
        ).filter(has_text=expected_value)

    def select_children(self, number):
        self.children_dropdown.click()
        try:
            option_locator = self.page.get_by_text(str(number), exact=True).nth(1)
            if option_locator.count() == 0:
                raise AssertionError(f"No children option with count {number} exists in the dropdown.")

            option_locator.click(timeout=2000)
        except TimeoutError:
            raise AssertionError(f"Timeout reached: No children option with count {number} exists in the dropdown.")

    def get_selected_children(self, expected_value):
        return self.children_dropdown.locator(
            "li.theme__selected___2Uc3r.WhiteDropDown__selected___3y0b0"
        ).filter(has_text=expected_value)

    def get_space_card_names(self):
        space_cards = self.page.locator("div[class*='GalleryItem__gallery-item']")
        space_names = []

        for i in range(space_cards.count()):
            card = space_cards.nth(i)
            name_element = card.locator("div[class*='GalleryItem__cardTitle']")

            if name_element.count() > 0:
                space_name = name_element.text_content().strip()
            else:
                full_text = card.text_content().strip()
                space_name = full_text.splitlines()[0]

            space_names.append(space_name)

        return space_names

    def load_more_space_cards(self):
        if self.load_more_button.is_visible():
            self.load_more_button.click()
            self.page.wait_for_timeout(1000)


    def navigate_to_destinations_section(self):
        self.page.locator("button:has-text('Select Destination')").click()
        expect(self.page).to_have_url("https://demo.testim.io/destinations")

    def book_first_destination(self):
        book_button = self.page.locator("div button:has-text('Book')").first
        book_button.click()

        return self.page.locator("div button:has-text('Booked')").first

    def get_space_card_prices(self):
        space_cards = self.page.locator("div[class*='GalleryItem__gallery-item']")
        space_prices = {}

        for i in range(space_cards.count()):
            card = space_cards.nth(i)
            if card.is_visible():
                try:
                    name_element = card.locator("div[class*='GalleryItem__cardTitle']")
                    price_element = card.locator("span.GalleryItem__price-tag___3q0Al")

                    if name_element.is_visible() and price_element.is_visible():
                        name = name_element.text_content(timeout=2000).strip()
                        price_text = price_element.text_content(timeout=2000).strip().replace("$", "")
                        price = float(price_text)
                        space_prices[name] = price
                except TimeoutError:
                    print(f"Failed to retrieve data for space card index {i}. Retrying...")
                    continue

        return space_prices

    def fill_target_price(self, price):
        self.target_price_locator.fill(price)

    def load_all_space_cards(self):
        while self.load_more_button.is_enabled():
            self.load_more_button.click()
            self.page.wait_for_timeout(500)

