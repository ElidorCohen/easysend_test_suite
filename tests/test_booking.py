import pytest
from playwright.sync_api import expect


@pytest.mark.sanity
# Will add parametrize for invalid dates later if I have more time
def test_fill_form_and_agree_to_terms(booking_page):
    booking_page.fill_form(
        name="John Doe",
        email="johndoe@example.com",
        ssn="123-45-6789",
        phone="13235993883",
        promo_code="PROMO2023"
    )

    booking_page.agree_to_terms()

    expect(booking_page.name_field).to_have_value("John Doe")
    expect(booking_page.email_field).to_have_value("johndoe@example.com")
    expect(booking_page.ssn_field).to_have_value("123-45-6789")
    expect(booking_page.phone_field).to_have_value("13235993883")
    expect(booking_page.promo_code_field).to_have_value("PROMO2023")
    expect(booking_page.terms_checkbox).to_be_checked()


@pytest.mark.sanity
@pytest.mark.parametrize("invalid_promos", ["     ", "123123", "PROMOINVALID", "RRRRR", "lowercase"])
def test_fake_promo_code_applies_discount(booking_page, invalid_promos):
    total_price = booking_page.get_total_price()
    booking_page.promo_code_field.fill(invalid_promos)

    booking_page.click_apply_button()

    updated_total_price = booking_page.get_total_price()

    assert total_price < updated_total_price, f"Expected total price to be {total_price}, but got {updated_total_price}."


@pytest.mark.sanity
@pytest.mark.parametrize("valid_promos", ["ValidPromo","PROMO2023", "PROMO2024", "PROMO2025", "PROMO2026"])
def test_apply_button_disabled_when_code_is_valid(booking_page, valid_promos):
    booking_page.promo_code_field.fill(valid_promos)
    booking_page.click_apply_button()

    expect(booking_page.apply_button).to_be_disabled()


@pytest.mark.sanity
def test_pay_now_button_disabled_when_terms_not_accepted(booking_page):
    booking_page.fill_form(
        name="John Doe",
        email="johndoe@example.com",
        ssn="123-45-6789",
        phone="13235993883",
        promo_code="PROMO2023"
    )

    expect(booking_page.pay_now_button).to_be_enabled()

    booking_page.click_pay_now()

    expect(booking_page.error_dialog).to_be_visible()


@pytest.mark.xfail(reason="When user uploads a file, the image placeholder of the file preview is not correct,"
                          "it shows a foreign unknown file preview constantly.")
@pytest.mark.sanity
def test_insurance_image_is_correct(booking_page):
    bugged_img_src = "/79d9840ec46e798f2430f6fca2c019de.jpg"

    booking_page.click_upload_box()
    booking_page.upload_file("test_files/insurance_test_file.pdf")

    image_placeholder = booking_page.page.locator("div.CustomerInfo__dropzone___3tqul img")
    expect(image_placeholder).to_be_visible()

    uploaded_img_src = image_placeholder.get_attribute("src")
    assert uploaded_img_src != bugged_img_src, f"Unexpected image src '{bugged_img_src}' displayed as preview."


@pytest.mark.xfail(reason="Users have the ability to upload any file, even corrupted files, without restrictions.")
@pytest.mark.sanity
def test_upload_corrupt_file_success(booking_page):
    booking_page.click_upload_box()
    booking_page.upload_file("test_files/corrupted_file_to_upload.curr")

    image_placeholder = booking_page.page.locator("div.CustomerInfo__dropzone___3tqul img")
    expect(image_placeholder).not_to_be_visible()


@pytest.mark.xfail(reason="Pay Now button clicked but no action occurred: no URL change, success message, or failure message.")
@pytest.mark.sanity
def test_pay_now_button_no_action(booking_page):
    booking_page.fill_form(
        name="John Doe",
        email="john.doe@example.com",
        ssn="123-45-6789",
        phone="13235993883",
        promo_code=""
    )
    booking_page.agree_to_terms()

    expect(booking_page.pay_now_button).to_be_enabled()

    booking_page.click_pay_now()

    assert booking_page.has_booking_action_occurred(), (
        "Pay Now button clicked but no action occurred: "
        "no URL change, success message, or failure message."
    )


@pytest.mark.sanity
@pytest.mark.parametrize("adults_count", [
    pytest.param(0, marks=pytest.mark.xfail(reason="Adults count of 0 is out of bounds")),
    1, 2, 3, 4,
    pytest.param(5, marks=pytest.mark.xfail(reason="Adults count of 5 is out of bounds"))
])
def test_price_increases_when_adding_adults(home_page, booking_page, adults_count):
    initial_total_price = booking_page.get_total_price()

    home_page.select_adults(adults_count)
    total_price_after_adults = booking_page.get_total_price()

    assert total_price_after_adults > initial_total_price, (
        f"Expected total price to increase after adding adults, but it did not. "
        f"Initial: {initial_total_price}, After adding adults: {total_price_after_adults}"
    )


@pytest.mark.sanity
@pytest.mark.parametrize("children_count", [
    pytest.param(0, marks=pytest.mark.xfail(reason="Adults count of 0 is out of bounds")),
    1, 2, 3, 4,
    pytest.param(5, marks=pytest.mark.xfail(reason="Adults count of 5 is out of bounds"))
])
def test_price_increases_when_adding_children(home_page, booking_page, children_count):
    initial_total_price = booking_page.get_total_price()

    home_page.select_children(children_count)
    total_price_after_children = booking_page.get_total_price()

    assert total_price_after_children > initial_total_price, (
        f"Expected total price to increase after adding children, but it did not. "
        f"Initial: {initial_total_price}, After adding children: {total_price_after_children}"
    )


@pytest.mark.sanity
@pytest.mark.parametrize("adults_count", [
    pytest.param(0, marks=pytest.mark.xfail(reason="Adults count of 0 is out of bounds")),
    pytest.param(1, marks=pytest.mark.xfail(reason="By default, there is at least 1 adult")),
    2, 3, 4,
    pytest.param(5, marks=pytest.mark.xfail(reason="Adults count of 5 is out of bounds"))
])
def test_travelers_count_increases_when_adding_adults(home_page, booking_page, adults_count):
    initial_travelers_count = booking_page.get_travelers_count()

    home_page.select_adults(adults_count)

    updated_travelers_count = booking_page.get_travelers_count()

    assert updated_travelers_count > initial_travelers_count, (
        f"Expected travelers count to increase after adding adults, but it did not. "
        f"Initial: {initial_travelers_count}, After adding adults: {updated_travelers_count}"
    )


@pytest.mark.sanity
@pytest.mark.parametrize("children_count", [
    pytest.param(0, marks=pytest.mark.xfail(reason="Children count of 0 is out of bounds")),
    1, 2, 3, 4,
    pytest.param(5, marks=pytest.mark.xfail(reason="Children count of 5 is out of bounds"))
])
def test_travelers_count_increases_when_adding_children(home_page, booking_page, children_count):
    initial_travelers_count = booking_page.get_travelers_count()

    home_page.select_children(children_count)
    updated_travelers_count = booking_page.get_travelers_count()

    assert updated_travelers_count >= initial_travelers_count + children_count, (
        f"Expected travelers count to increase by {children_count} after adding children, but it did not. "
        f"Initial: {initial_travelers_count}, After adding children: {updated_travelers_count}"
    )


