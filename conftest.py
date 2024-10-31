import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from pages.home_page import HomePage
from pages.website import Website
from playwright.sync_api import Browser, BrowserContext, Page, expect
from pages.booking_page import BookingPage


load_dotenv()


@pytest.fixture(scope="session")
def browser():
    base_url = os.getenv("BASE_URL")
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)
        context: BrowserContext = browser.new_context(base_url=base_url)
        yield context
        context.close()
        browser.close()


@pytest.fixture
def website(browser):
    page: Page = browser.new_page()
    page.goto("/")
    website = Website(page)
    yield website
    page.close()


@pytest.fixture
def home_page(website):
    home_page = HomePage(website.page)
    yield home_page


@pytest.fixture
def login_page(website):
    login_page = website.goto_login()
    yield login_page


@pytest.fixture
def booking_page(home_page):
    home_page.navigate_to_destinations_section()
    home_page.book_first_destination()

    expect(home_page.page).to_have_url("https://demo.testim.io/checkout")

    booking_page = BookingPage(home_page.page)
    yield booking_page
