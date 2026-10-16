from datetime import date, timedelta

import config
import flows
from pages.base_page import BasePage
from pages.patient_pages import PatientDashboardPage


def test_search_by_specialization_filters_doctors(driver):
    flows.login_as(driver, config.PATIENT)
    dashboard = PatientDashboardPage(driver)
    dashboard.search("Derm")
    names = dashboard.doctor_names()
    assert config.DOCTOR2["name"] in names
    assert config.DOCTOR["name"] not in names


def test_search_with_no_match_shows_empty_state(driver):
    flows.login_as(driver, config.PATIENT)
    dashboard = PatientDashboardPage(driver)
    dashboard.search("zzzz-no-such-specialty")
    assert dashboard.has_no_results()
    assert dashboard.doctor_names() == []


def test_new_patient_starts_with_no_appointments(driver, patient):
    flows.login_as(driver, patient)
    dashboard = PatientDashboardPage(driver)
    assert dashboard.appointment_rows() == []
    assert dashboard.has_empty_state()
    assert "Cart" not in dashboard.body_text      # leftover shopping-site wording


def test_book_a_slot(driver, patient):
    slot = flows.create_slot(driver)
    dashboard = flows.book_as(driver, patient, slot)
    row = dashboard.appointment_row(slot["date"])
    assert config.DOCTOR_NAME in row.text
    assert "confirmed" in row.text.lower()


def test_cancel_frees_the_slot(driver, patient):
    slot = flows.create_slot(driver, capacity=1)
    dashboard = flows.book_as(driver, patient, slot)
    dashboard.cancel_appointment(slot["date"])
    dashboard.wait_for_flash("success", "Appointment cancelled.")
    row = dashboard.appointment_row(slot["date"])
    assert "cancelled" in row.text.lower()
    assert not row.find_elements(*dashboard.CANCEL_BUTTON)
    assert "booked: 0/1" in flows.open_doctor_page(driver).card(slot).text.lower()


def test_can_rebook_after_cancelling(driver, patient):
    slot = flows.create_slot(driver, capacity=1)
    dashboard = flows.book_as(driver, patient, slot)
    dashboard.cancel_appointment(slot["date"])
    dashboard.wait_for_flash("success", "Appointment cancelled.")
    flows.open_doctor_page(driver).book(slot)
    dashboard.wait_for_flash("success", "Appointment booked successfully.")


def test_full_slot_cannot_be_booked_by_another_patient(driver, patient):
    slot = flows.create_slot(driver, capacity=1)
    flows.book_as(driver, patient, slot)
    flows.logout(driver)
    other = flows.register_patient(driver)
    flows.login_as(driver, other)
    detail = flows.open_doctor_page(driver)
    assert detail.is_full(slot)
    assert not detail.has_book_button(slot)


def test_same_patient_cannot_book_a_slot_twice(driver, patient):
    slot = flows.create_slot(driver, capacity=2)
    flows.book_as(driver, patient, slot)
    detail = flows.open_doctor_page(driver)
    detail.book(slot)
    detail.wait_for_flash("error", "You already have a booking for this slot.")


def test_past_slots_are_not_listed(driver, patient):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    slot = flows.create_slot(driver, date_iso=yesterday, start="13:00", end="13:30")
    flows.login_as(driver, patient)
    assert not flows.open_doctor_page(driver).has_slot(slot)


def test_cqa1_duplicate_booking_of_own_full_slot_says_already_booked(driver, patient):
    """Regression for CQA-1. A stale page replays the booking POST for a slot the same
    patient already filled. The user must be told 'you already have a booking', not
    'slot is fully booked'."""
    slot = flows.create_slot(driver, capacity=1)
    flows.login_as(driver, patient)
    detail = flows.open_doctor_page(driver)
    action = detail.book_action(slot)
    detail.book(slot)
    PatientDashboardPage(driver).wait_for_flash("success", "Appointment booked successfully.")

    detail = flows.open_doctor_page(driver)
    detail.replay_post(action)
    detail.wait_for_flash("error", "You already have a booking for this slot.")
    assert "fully booked" not in BasePage(driver).body_text
