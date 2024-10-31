import re
from playwright.sync_api import expect
from pages.base_page import BasePage


class BookingPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.name_field = page.locator("input[type='text'][maxlength='30']")
        self.email_field = self.page.locator("input[type='email']")
        self.ssn_field = page.locator("div").filter(has_text=re.compile(r"^Social Security Number$")).locator("input")
        self.phone_field = self.page.locator("input[type='tel']")
        self.promo_code_field = self.page.locator("input[name='promo']")
        self.destination_button = "#select-destination"
        self.terms_checkbox = self.page.locator("label").filter(has_text="I agree to the terms and").locator("div")
        self.total_price_locator = self.page.locator("div:has-text('Total') strong")
        self.apply_button = self.page.locator("button:has-text('Apply')")
        self.pay_now_button = self.page.locator("button:has-text('Pay now')")
        self.error_dialog = self.page.locator("div[data-react-toolbox='dialog']")
        self.dropzone_box = self.page.locator("div[class*='CustomerInfo__dropzone-box___27VMo']")
        self.file_input = self.page.locator("input[type='file']")

    def agree_to_terms(self):
        self.terms_checkbox.click()

    def fill_form(self, name, email, ssn, phone, promo_code):
        self.name_field.fill(name)
        self.email_field.fill(email)
        self.ssn_field.fill(ssn)
        self.phone_field.fill(phone)
        self.promo_code_field.fill(promo_code)

    def get_total_price(self):
        price_text = self.total_price_locator.text_content().strip().replace("$", "")
        return price_text

    def click_pay_now(self):
        self.pay_now_button.click()

    def is_error_dialog_visible(self):
        return self.error_dialog.is_visible()

    def get_error_dialog_text(self):
        if self.is_error_dialog_visible():
            return self.error_dialog.text_content().strip()
        return None

    def click_apply_button(self):
        self.apply_button.click()

    def click_upload_box(self):
        self.dropzone_box.click()

    def upload_file(self, file_path):
        self.file_input.set_input_files(file_path)

    def has_booking_action_occurred(self, timeout_ms=3000):
        try:
            expect(self.page).to_have_url("https://demo.testim.io/confirmation", timeout=timeout_ms)
            return True
        except Exception:
            pass

        return (
                self.page.locator("text='Booking confirmed!'").is_visible() or
                self.page.locator("text='Payment failed.'").is_visible()
        )

    def get_travelers_count(self):
        for count in range(1, 8):
            traveler_text = f"{count} traveler" if count == 1 else f"{count} travelers"

            try:
                traveler_text_content = self.page.get_by_text(traveler_text, exact=True).text_content(timeout=2000).strip()

                match = re.match(r"(\d+) traveler[s]?", traveler_text_content)
                if match:
                    travelers_count = int(match.group(1))
                    return travelers_count

            except Exception:
                continue

        raise ValueError("Travelers count not found on the page.")




