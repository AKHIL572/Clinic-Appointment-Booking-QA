import uuid

import pytest

import config
import flows
from pages.admin_pages import AdminDashboardPage
from pages.base_page import by_testid


def test_admin_can_add_a_doctor_who_can_then_log_in(driver):
    suffix = uuid.uuid4().hex[:6]
    doctor = {"name": f"Dr. QA {suffix}", "email": f"doc_{suffix}@clinic.test",
              "password": "DoctorPass123", "path": "/doctor/dashboard"}
    flows.login_as(driver, config.ADMIN)
    dashboard = AdminDashboardPage(driver)
    dashboard.click_add_doctor().create(doctor["name"], doctor["email"], "QA Testing", doctor["password"])
    dashboard.wait_for_flash("success", "Doctor created.")
    assert dashboard.doctor_rows(doctor["name"])

    flows.logout(driver)
    flows.login_as(driver, doctor)


def test_admin_cannot_add_doctor_with_duplicate_email(driver):
    flows.login_as(driver, config.ADMIN)
    dashboard = AdminDashboardPage(driver)
    dashboard.click_add_doctor().create("Dr. Copy", config.DOCTOR["email"], "Anything", "DoctorPass123")
    dashboard.wait_for_flash("error", "A user with this email already exists.")


def test_cqa2_admin_dashboard_lists_slots_and_who_booked(driver, patient):
    """Regression for CQA-2: existing slots must be visible on the admin dashboard."""
    slot = flows.create_slot(driver, capacity=2)
    flows.login_as(driver, config.ADMIN)
    dashboard = AdminDashboardPage(driver)
    rows = dashboard.slot_rows(slot["date"])
    assert len(rows) == 1
    assert config.DOCTOR_NAME in rows[0].text
    assert "0 / 2" in rows[0].text
    flows.logout(driver)

    flows.book_as(driver, patient, slot)
    flows.logout(driver)
    flows.login_as(driver, config.ADMIN)
    row = AdminDashboardPage(driver).slot_rows(slot["date"])[0]
    assert "1 / 2" in row.text
    assert patient["name"] in row.text


@pytest.mark.xfail(strict=True,
                   reason="Known limitation: slot time format is not validated "
                          "(see Test Closure Report). Remove this marker once it is fixed.")
def test_slot_with_invalid_time_format_is_rejected(driver):
    flows.login_as(driver, config.ADMIN)
    dashboard = AdminDashboardPage(driver)
    page = dashboard.click_add_slot_for(config.DOCTOR2["name"])
    page.create(flows.random_future_date(), "25:99", "not-a-time", 1)
    page.wait.until(lambda d: d.find_elements("css selector", "[data-testid^='flash-']"))
    assert page.driver.find_elements(*by_testid("flash-error")), "App accepted an invalid time"
