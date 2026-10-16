import pytest

import config
import flows
from pages.auth_pages import LoginPage, RegisterPage
from pages.base_page import BasePage


@pytest.mark.parametrize("user", [config.PATIENT, config.DOCTOR, config.ADMIN],
                         ids=["patient", "doctor", "admin"])
def test_login_lands_on_role_dashboard(driver, user):
    page = flows.login_as(driver, user)
    assert page.path == user["path"]
    assert user["name"] in page.logged_in_name()


@pytest.mark.parametrize("email,password", [
    (config.PATIENT["email"], "WrongPassword1"),
    ("nobody@clinic.test", "PatientPass123"),
], ids=["wrong-password", "unknown-email"])
def test_invalid_login_shows_error(driver, email, password):
    LoginPage(driver).open_page().login(email, password)
    page = BasePage(driver)
    page.wait_for_flash("error", "Incorrect email or password.")
    assert page.path == "/login"


def test_empty_login_is_blocked_by_the_browser(driver):
    login = LoginPage(driver).open_page()
    login.submit_empty()
    assert login.path == "/login"


def test_register_then_login(driver):
    patient = flows.register_patient(driver)
    page = flows.login_as(driver, patient)
    assert patient["name"] in page.logged_in_name()


def test_register_with_existing_email_is_rejected(driver):
    RegisterPage(driver).open_page().register("Someone Else", config.PATIENT["email"], "PatientPass123")
    BasePage(driver).wait_for_flash("error", "An account with this email already exists.")


def test_register_with_short_password_is_blocked(driver):
    register = RegisterPage(driver).open_page()
    register.register("Short Pass", "short_pw@clinic.test", "abc123")
    assert register.path == "/register"
    assert register.password_validation_message() != ""


def test_logout_ends_the_session(driver):
    flows.login_as(driver, config.PATIENT)
    flows.logout(driver)
    page = BasePage(driver)
    page.visit("/patient/dashboard")
    assert "Patient Dashboard" not in page.body_text
