import pytest
from playwright.sync_api import expect, sync_playwright


@pytest.mark.sanity
@pytest.mark.parametrize("username, password", [
    ("validUsername", "validPassword"),
    ("usr", "p"),
    ("abc", "xYz123!"),
    ("AAA", "Z"),
])
def test_successful_login(login_page, username, password):
    login_page.fill_credentials(username, password)
    home_page = login_page.submit()

    expect(home_page.page).to_have_url('https://demo.testim.io/')
    expect(home_page.page.locator("button span:has-text('Hello, John')")).to_be_visible()


@pytest.mark.sanity
@pytest.mark.parametrize("username, password, error_message", [
    ("s", "p", "Name is a required field."),
    ("", "p", "Name is a required field."),
    ("$%", "p", "Name is a required field."),
])
def test_login_invalid_username(login_page, username, password, error_message):
    login_page.fill_credentials(username, password)
    login_page.submit()

    login_page.check_username_error(error_message)
    expect(login_page.page).not_to_have_url("https://demo.testim.io/")


@pytest.mark.sanity
@pytest.mark.parametrize("username, password, error_message", [
    ("validUsername", "", "Password is a required field."),
    ("123", "", "Password is a required field."),
    ("   ", "", "Password is a required field."),
])
def test_login_invalid_password(login_page, username, password, error_message):
    login_page.fill_credentials(username, password)
    login_page.submit()

    login_page.check_password_error(error_message)
    expect(login_page.page).not_to_have_url("https://demo.testim.io/")


@pytest.mark.sanity
def test_login_empty_fields(login_page):
    login_page.fill_credentials("", "")
    login_page.submit()

    login_page.check_username_error("Name is a required field.")
    login_page.check_password_error("Password is a required field.")
    expect(login_page.page).not_to_have_url("https://demo.testim.io/")


@pytest.mark.sanity
@pytest.mark.parametrize("username, password, error_message", [
    ("", "123", "Name is a required field."),
    ("", "asd", "Name is a required field."),
    ("", "@#$", "Name is a required field."),
])
def test_login_only_password_filled(login_page, username, password, error_message):
    login_page.fill_credentials(username, password)
    login_page.submit()

    login_page.check_username_error(error_message)
    expect(login_page.page).not_to_have_url("https://demo.testim.io/")


@pytest.mark.xfail(reason="Login isn't persistent after reload")
@pytest.mark.sanity
def test_session_persistence_after_login(login_page):
    login_page.fill_credentials("validUsername", "p")
    home_page = login_page.submit()

    expect(home_page.page).to_have_url("https://demo.testim.io/")
    home_page.page.reload()

    assert login_page.is_login_persistent(), "Login session persisted unexpectedly after reload."


