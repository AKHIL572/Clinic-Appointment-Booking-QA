import config
import flows
from pages.base_page import by_qa
from pages.doctor_pages import DoctorDashboardPage
from pages.patient_pages import PatientDashboardPage


def test_doctor_sees_booking_and_marks_it_complete(driver, patient):
    slot = flows.create_slot(driver)
    flows.book_as(driver, patient, slot)
    flows.logout(driver)

    flows.login_as(driver, config.DOCTOR)
    dashboard = DoctorDashboardPage(driver)
    assert "confirmed" in dashboard.row_for(patient["name"]).text.lower()

    dashboard.complete(patient["name"])
    dashboard.wait_for_flash("success", "Appointment marked complete.")
    row = dashboard.row_for(patient["name"])
    assert "completed" in row.text.lower()
    assert not row.find_elements(*by_qa("complete-button"))

    flows.logout(driver)
    flows.login_as(driver, patient)
    patient_row = PatientDashboardPage(driver).appointment_row(slot["date"])
    assert "completed" in patient_row.text.lower()
    assert not patient_row.find_elements(*PatientDashboardPage.CANCEL_BUTTON)


def test_doctor_only_sees_their_own_patients(driver, patient):
    slot = flows.create_slot(driver, doctor_name=config.DOCTOR2["name"])
    flows.book_as(driver, patient, slot)
    flows.logout(driver)

    flows.login_as(driver, config.DOCTOR)           # Dr. Anjali: must NOT see it
    assert DoctorDashboardPage(driver).rows_matching(patient["name"]) == []
    flows.logout(driver)

    flows.login_as(driver, config.DOCTOR2)          # Dr. Rahul: must see it
    assert DoctorDashboardPage(driver).rows_matching(patient["name"])


def test_cqa3_doctor_name_has_no_duplicated_prefix(driver):
    """Regression for CQA-3 ('Dr. Dr. ...' after the UI redesign)."""
    flows.login_as(driver, config.PATIENT)
    dashboard_text = PatientDashboardPage(driver).body_text
    assert config.DOCTOR_NAME in dashboard_text
    assert "Dr. Dr." not in dashboard_text
    assert "Dr. Dr." not in flows.open_doctor_page(driver).body_text
    flows.logout(driver)

    flows.login_as(driver, config.DOCTOR)
    assert "Dr. Dr." not in DoctorDashboardPage(driver).body_text
