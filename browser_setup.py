import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Browser, BrowserContext

load_dotenv()


def create_browser_context() -> BrowserContext:
    base_url = os.getenv("BASE_URL")
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)
        context: BrowserContext = browser.new_context(base_url=base_url)
        return context
