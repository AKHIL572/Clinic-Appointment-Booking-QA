from selenium.webdriver.common.by import By

from pages.base_page import BasePage, by_qa


class LoginPage(BasePage):
    EMAIL = (By.ID, "login-email")
    PASSWORD = (By.ID, "login-password")
    BUTTON = by_qa("login-button")

    def open_page(self):
        self.visit("/login")
        return self

    def login(self, email, password):
        self.type_into(self.EMAIL, email)
        self.type_into(self.PASSWORD, password)
        self.click(self.BUTTON)
        return self

    def submit_empty(self):
        self.click(self.BUTTON)


class RegisterPage(BasePage):
    NAME = (By.ID, "signup-name")
    EMAIL = (By.ID, "signup-email")
    PASSWORD = (By.ID, "signup-password")
    BUTTON = by_qa("signup-button")

    def open_page(self):
        self.visit("/register")
        return self

    def register(self, name, email, password):
        self.type_into(self.NAME, name)
        self.type_into(self.EMAIL, email)
        self.type_into(self.PASSWORD, password)
        self.click(self.BUTTON)
        return self

    def password_validation_message(self):
        """The browser's own HTML5 validation message (minlength=8) for the password box."""
        return self.driver.find_element(*self.PASSWORD).get_attribute("validationMessage")
