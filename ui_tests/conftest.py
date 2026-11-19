import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import config
import flows


@pytest.fixture
def driver():
    options = Options()
    if config.HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,900")
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


@pytest.fixture
def patient(driver):
    """A brand-new patient account, registered through the UI."""
    return flows.register_patient(driver)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot whenever a test fails, to make failures easy to diagnose."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        if browser:
            os.makedirs("screenshots", exist_ok=True)
            browser.save_screenshot(os.path.join("screenshots", f"{item.name}.png"))
