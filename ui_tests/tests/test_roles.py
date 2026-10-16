import pytest

import config
import flows
from pages.base_page import BasePage

ADMIN_ONLY = "Forbidden: admin access only"
DOCTOR_ONLY = "Forbidden: doctor access only"
PATIENT_ONLY = "Forbidden: patient access only"


@pytest.mark.parametrize("user,path,message", [
    (config.PATIENT, "/admin/dashboard", ADMIN_ONLY),
    (config.PATIENT, "/doctor/dashboard", DOCTOR_ONLY),
    (config.DOCTOR, "/admin/dashboard", ADMIN_ONLY),
    (config.DOCTOR, "/patient/dashboard", PATIENT_ONLY),
    (config.ADMIN, "/doctor/dashboard", DOCTOR_ONLY),
    (config.ADMIN, "/patient/dashboard", PATIENT_ONLY),
], ids=["patient->admin", "patient->doctor", "doctor->admin",
        "doctor->patient", "admin->doctor", "admin->patient"])
def test_role_cannot_open_other_roles_pages(driver, user, path, message):
    flows.login_as(driver, user)
    page = BasePage(driver)
    page.visit(path)
    assert message in page.body_text


@pytest.mark.parametrize("path", ["/patient/dashboard", "/doctor/dashboard", "/admin/dashboard"])
def test_anonymous_user_cannot_open_dashboards(driver, path):
    page = BasePage(driver)
    page.visit(path)
    assert "Dashboard" not in page.body_text
