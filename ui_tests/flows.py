"""Reusable multi-step actions so tests stay short and readable.
Every flow that needs data creates its own (fresh patient, fresh slot), so tests do not
depend on each other or on how much of the seeded data earlier runs used up."""
import random
import uuid
from datetime import date, timedelta

import config
from pages.admin_pages import AdminDashboardPage
from pages.auth_pages import LoginPage, RegisterPage
from pages.base_page import BasePage
from pages.patient_pages import PatientDashboardPage


def random_future_date():
    """A unique far-future ISO date, so each test's slot is easy to find and never collides."""
    return (date.today() + timedelta(days=random.randint(60, 9000))).isoformat()


def login_as(driver, user):
    LoginPage(driver).open_page().login(user["email"], user["password"])
    page = BasePage(driver)
    page.wait_for_path(user["path"])
    return page


def logout(driver):
    BasePage(driver).logout()


def register_patient(driver):
    suffix = uuid.uuid4().hex[:8]
    patient = {"name": f"QA Patient {suffix}", "email": f"qa_{suffix}@clinic.test",
               "password": "PatientPass123", "path": "/patient/dashboard"}
    RegisterPage(driver).open_page().register(patient["name"], patient["email"], patient["password"])
    BasePage(driver).wait_for_flash("success", "Registration successful")
    return patient


def create_slot(driver, doctor_name=config.DOCTOR_NAME, capacity=1,
                start="09:00", end="09:30", date_iso=None):
    """Log in as admin, add a slot through the UI, log out. Returns the slot's details."""
    slot = {"doctor": doctor_name, "date": date_iso or random_future_date(),
            "start": start, "end": end, "capacity": capacity}
    login_as(driver, config.ADMIN)
    dashboard = AdminDashboardPage(driver)
    page = dashboard.click_add_slot_for(doctor_name)
    page.create(slot["date"], start, end, capacity)
    dashboard.wait_for_flash("success", "Slot added.")
    logout(driver)
    return slot


def open_doctor_page(driver, doctor_name=config.DOCTOR_NAME):
    """From any patient page, open a doctor's slot list."""
    return PatientDashboardPage(driver).open_page().open_doctor(doctor_name)


def book_as(driver, patient, slot):
    """Log in as the patient and book the slot. Ends on the patient dashboard."""
    login_as(driver, patient)
    open_doctor_page(driver, slot["doctor"]).book(slot)
    dashboard = PatientDashboardPage(driver)
    dashboard.wait_for_flash("success", "Appointment booked successfully.")
    return dashboard
