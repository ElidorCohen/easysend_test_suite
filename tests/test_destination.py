import pytest
from playwright.sync_api import expect


@pytest.mark.sanity
def test_book_button_changes_to_booked(home_page):
    home_page.navigate_to_destinations_section()

    book_button = home_page.book_first_destination()
    expect(book_button).to_have_text("Booked")


@pytest.mark.sanity
def test_navigation_to_checkout(home_page):
    home_page.navigate_to_destinations_section()

    home_page.book_first_destination()
    expect(home_page.page).to_have_url("https://demo.testim.io/checkout")


@pytest.mark.sanity
def test_load_more_space_cards(home_page):
    initial_count = len(home_page.get_space_card_names())
    home_page.load_more_space_cards()

    updated_count = len(home_page.get_space_card_names())
    assert updated_count > initial_count, f"Expected more than {initial_count} cards, but got {updated_count}"


@pytest.mark.sanity
@pytest.mark.parametrize("target_price", [50, 100, 150, 450, 1800, 1900])
def test_slider_filters_space_cards_by_price(home_page, target_price):
    home_page.load_all_space_cards()
    home_page.get_space_card_prices()

    home_page.fill_target_price(str(target_price))
    home_page.page.keyboard.press("Enter")

    filtered_space_cards = home_page.get_space_card_prices()

    for name, price in filtered_space_cards.items():
        assert price <= target_price, f"Space card '{name}' has price {price} which exceeds the target price of {target_price}"

