from urllib.parse import urlparse

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


def by_qa(name):
    """Locator for the app's data-qa='...' test hooks."""
    return (By.CSS_SELECTOR, f"[data-qa='{name}']")


def by_testid(name):
    """Locator for the app's data-testid='...' test hooks."""
    return (By.CSS_SELECTOR, f"[data-testid='{name}']")


class BasePage:
    """Shared helpers. Every page object inherits these."""

    LOGOUT = (By.ID, "logout-link")
    USER_PILL = (By.CSS_SELECTOR, ".user-pill")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.TIMEOUT,
                                  ignored_exceptions=(StaleElementReferenceException,))

    # ---- navigation / state -------------------------------------------------
    def visit(self, path):
        self.driver.get(config.BASE_URL + path)

    @property
    def path(self):
        return urlparse(self.driver.current_url).path

    @property
    def body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def wait_for_path(self, path):
        self.wait.until(lambda d: urlparse(d.current_url).path == path,
                        message=f"Never reached {path}; stuck on {self.driver.current_url}")

    # ---- element helpers (all use explicit waits, never sleep) -------------
    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_into(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def find_xpath(self, xpath):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def find_all_xpath(self, xpath):
        return self.driver.find_elements(By.XPATH, xpath)

    # ---- flash messages ------------------------------------------------------
    def wait_for_flash(self, category, text):
        """Wait until a flash message of this category containing `text` is on screen.
        Checking the text (not just presence) avoids reading a stale message from the
        previous page."""
        locator = by_testid(f"flash-{category}")
        try:
            self.wait.until(lambda d: any(text in e.text for e in d.find_elements(*locator)))
        except TimeoutException:
            seen = [e.text for e in self.driver.find_elements(*locator)]
            raise AssertionError(
                f"Expected a '{category}' message containing {text!r}, saw {seen}") from None

    # ---- session -------------------------------------------------------------
    def logout(self):
        self.click(self.LOGOUT)
        self.wait_for_path("/login")

    def logged_in_name(self):
        return self.find(self.USER_PILL).text
