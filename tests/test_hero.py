import pytest
from playwright.sync_api import expect


@pytest.mark.sanity
def test_select_destination_navigation(home_page):
    select_destination_button = home_page.page.locator("button:has-text('Select Destination')")
    select_destination_button.click()

    expect(home_page.page).to_have_url("https://demo.testim.io/destinations")


@pytest.mark.xfail(reason="Year isn't being updated according to the selected year.")
@pytest.mark.sanity
@pytest.mark.parametrize("year", ["2022", "2023", "2024", "2025", "2026"])
def test_select_year(home_page, year):
    home_page.open_date_picker("departing")
    home_page.select_year(year)

    expect(home_page.page.locator("span#years")).to_have_text(year)


@pytest.mark.sanity
@pytest.mark.parametrize("month", ["January", "February", "March", "April", "May", "June", "July",
                                   "August", "September", "October", "November", "December"])
def test_select_month(home_page, month):
    home_page.open_date_picker("departing")
    home_page.select_month(month)

    expect(home_page.month_locator).to_contain_text(month)


@pytest.mark.sanity
@pytest.mark.parametrize("year, month, day", [
    ("2024", "11", "1"),
    ("2024", "11", "2"),
    ("2024", "11", "15"),
    ("2024", "11", "28"),
    ("2024", "11", "29"),
    ("2024", "11", "30"),
])
def test_select_valid_day(home_page, year, month, day):
    home_page.open_date_picker("departing")
    home_page.select_year(year)
    home_page.select_month("November")

    home_page.select_day(year, month, day)
    expect(home_page.page.locator(".theme__active___2k63V")).to_contain_text(day)


@pytest.mark.sanity
@pytest.mark.parametrize("year, month, day", [
    ("2024", "11", "0"),
    ("2024", "11", "31"),
    ("2024", "11", "32"),
])
def test_select_invalid_day(home_page, year, month, day):
    home_page.open_date_picker("departing")
    home_page.select_year(year)
    home_page.select_month("November")

    try:
        home_page.select_day(year, month, day)
    except ValueError as e:
        print(e)


@pytest.mark.sanity
@pytest.mark.parametrize("date_input, expected_value", [
    ("01/11/2024", "1 November 2024"),
    ("15/11/2024", "15 November 2024"),
    ("30/11/2024", "30 November 2024"),
    ("01/12/2024", "1 December 2024"),
    ("31/12/2024", "31 December 2024"),
    ("01/01/2025", "1 January 2025"),
    ("31/01/2025", "31 January 2025"),
    ("28/02/2025", "28 February 2025"),
])
def test_departing_valid_dates(home_page, date_input, expected_value):
    home_page.set_departing(date_input)
    home_page.submit_selection()
    expect(home_page.page.locator("input[type=\"text\"]").nth(0)).to_have_value(expected_value)


@pytest.mark.sanity
@pytest.mark.parametrize("date_input, expected_value", [
    ("31/11/2024", ""),
    ("29/02/2025", ""),
    ("31/04/2025", ""),
    ("0/11/2024", ""),
    ("15/13/2024", ""),
])
def test_departing_invalid_dates(home_page, date_input, expected_value):
    day, month, year = date_input.split("/")
    if home_page.select_day(day, month, year):
        home_page.set_departing(date_input)
        home_page.submit_selection()
    expect(home_page.page.locator("input[type=\"text\"]").nth(0)).to_have_value(expected_value)


@pytest.mark.sanity
@pytest.mark.parametrize("date_input, expected_value", [
    ("01/11/2024", "1 November 2024"),
    ("15/11/2024", "15 November 2024"),
    ("30/11/2024", "30 November 2024"),
    ("01/12/2024", "1 December 2024"),
    ("31/12/2024", "31 December 2024"),
    ("01/01/2025", "1 January 2025"),
    ("31/01/2025", "31 January 2025"),
    ("28/02/2025", "28 February 2025"),
])
def test_returning_valid_dates(home_page, date_input, expected_value):
    home_page.set_returning(date_input)
    home_page.submit_selection()
    expect(home_page.page.locator("input[type=\"text\"]").nth(1)).to_have_value(expected_value)


@pytest.mark.sanity
@pytest.mark.parametrize("date_input, expected_value", [
    ("31/11/2024", "Returning"),
    ("29/02/2025", "Returning"),
    ("31/04/2025", "Returning"),
    ("0/12/2024", "Returning"),
])
def test_returning_invalid_dates(home_page, date_input, expected_value):
    home_page.set_returning(date_input)
    home_page.submit_selection()
    expect(home_page.page.locator("input[type=\"text\"]").nth(1)).not_to_have_value(expected_value)


@pytest.mark.sanity
@pytest.mark.parametrize("adults_count", [
    pytest.param(0, marks=pytest.mark.xfail(reason="Adults count of 0 is out of bounds")),
    1, 2, 3, 4,
    pytest.param(5, marks=pytest.mark.xfail(reason="Adults count of 5 is out of bounds"))
])
def test_adults_dropdown(home_page, adults_count):
    home_page.select_adults(adults_count)

    selected_value_locator = home_page.get_selected_adults(str(adults_count))
    expect(selected_value_locator).to_have_text(str(adults_count))


@pytest.mark.sanity
@pytest.mark.parametrize("children_count", [
    pytest.param(0, marks=pytest.mark.xfail(reason="Children count of 0 is out of bounds")),
    1, 2, 3, 4,
    pytest.param(5, marks=pytest.mark.xfail(reason="Children count of 5 is out of bounds"))
])
def test_children_dropdown(home_page, children_count):
    home_page.select_children(children_count)

    selected_value_locator = home_page.get_selected_children(str(children_count))
    expect(selected_value_locator).to_have_text(str(children_count))






