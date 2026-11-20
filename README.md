# Clinic Appointment Booking System

**An End-to-End QA Portfolio Project: Manual STLC, Jira Agile Process & Selenium/pytest UI Automation**

[![UI Test Automation](https://github.com/AKHIL572/clinic-appointment-booking-qa/actions/workflows/ui-tests.yml/badge.svg)](https://github.com/AKHIL572/clinic-appointment-booking-qa/actions/workflows/ui-tests.yml)

**Status:** ✅ Completed (QA Cycle Closed — v1.0 → v1.1 + Post-Closure UI Automation Suite)  
**Role:** QA Analyst & Automation Engineer (also built the application under test)
**Type:** Manual + API Testing, UI Test Automation (POM), Defect Lifecycle Management, Agile QA Process  

---

## 🎯 Purpose & Overview

This project demonstrates a complete, independent **Software Testing Life Cycle (STLC)** conducted on a purpose-built, multi-role clinic application — rather than a generic public demo site. Every requirement, test case, defect, root-cause investigation, and automated test reflects genuine, end-to-end QA engineering.

Originally inspired by requirements gathering for an Ayurvedic healthcare clinic (BRD/SRS domain), the system was built and tested to simulate real-world healthcare scheduling challenges: role segregation, slot contention, schedule visibility, and prescription document handling.

---

## 🚀 Key Objectives

- **Full STLC Ownership:** Drive testing from requirements analysis, test strategy, and test plan design through execution, defect resolution, and formal test closure.
- **Agile QA in Jira:** Manage testing with Scrum artifacts (5 Epics, 15 Tasks, Releases v1.0 & v1.1, Labels, and Defect tracking).
- **Comprehensive Functional & API Validation:** Execute 41 structured manual and API test cases tracked with a live formula-driven Requirement Traceability Matrix (RTM).
- **Defect Lifecycle Management:** Uncover, report, triage, verify fixes, and formally close defects (CQA-1, CQA-2, CQA-3) through full lifecycles in Jira.
- **Root-Cause Investigation:** Use browser DevTools and direct SQLite database inspection scripts to distinguish genuine defects from environmental or data discrepancies.
- **UI Test Automation Framework:** Build a modular test automation suite using **Python, pytest, Selenium WebDriver, and the Page Object Model (POM)** with 39 collected tests.
- **Continuous Integration (CI):** Run automated test suites headlessly in cloud containers on every push and pull request via **GitHub Actions** with failure artifact capture.

---

## 🏥 Application Under Test

A multi-role healthcare scheduling platform built with Flask, SQLAlchemy, and SQLite:

### 1. Patient Portal
- User registration and authenticated login with session handling.
- Doctor discovery with real-time search filtering by medical specialization.
- Slot browsing, real-time availability checks, booking, and cancellation.
- The patient dashboard offers prescription uploads for appointments not marked cancelled (PDF, JPG, JPEG, or PNG; 5 MiB request-size limit).

### 2. Doctor Portal
- Dedicated schedule dashboard listing upcoming patient appointments.
- Status management (marking appointments as completed).
- Strict role isolation (doctors can only view their own appointments).

### 3. Admin Panel
- Doctor profile creation with duplicate email conflict prevention.
- Slot allocation management (specifying doctor, date, time window, and capacity).
- System-wide visibility of all doctors, allocated slots, and booked patients.

### 4. REST API Layer
- JSON endpoints for registration, login/logout, doctor and slot discovery, appointment booking/listing, and cancellation. Appointment actions require a login session: `POST /api/register`, `POST /api/login`, `POST /api/logout`, `GET /api/doctors`, `GET /api/doctors/<doctor_id>/slots`, `POST|GET /api/appointments`, and `POST /api/appointments/<appointment_id>/cancel`.

---

## 🧪 Testing Methodology & Scope

### 1. Test Planning & Documentation
The `docs/` folder contains the following QA artifacts:
- **[Test Strategy & Test Plan](docs/Test_Strategy_and_Test_Plan.docx):** This file currently contains a legacy e-commerce plan (automationexercise.com / reqres.in), not a clinic-app strategy; it should not be treated as current clinic documentation.
- **[Requirement Traceability Matrix & Test Repository](docs/QA_Test_Cases_and_RTM.xlsx):** 41 manual & API test cases mapped 1-to-1 with functional requirements, formula-driven metrics, and defect cross-references.
- **[Test Closure Report](docs/Test_Closure_Report.docx):** Formal exit criteria evaluation, defect resolution audit, and post-closure automation addendum.

### 2. Jira Agile Workflow
- **Epics (5):** Authentication, Slot Booking, Doctor Dashboard, Admin Panel, REST API Layer.
- **Tasks (15):** 3 Tasks per Epic (Test Design, Environment Setup, Execution).
- **Releases:** `v1.0 Baseline` and `v1.1 Post-Redesign & Fixes`.
- **Labels:** Utilized in place of components for modular filtering across the team-managed Scrum space.

### 3. Investigation & Diagnostic Integrity
Suspected anomalies were rigorously investigated using direct technical evidence before logging tickets:
- DOM structure inspected via Chrome DevTools to verify element states and flash messaging.
- Database state validated using custom Python inspection scripts (`inspect_db.py`, `inspect_users.py`) to confirm whether data was properly committed or if discrepancies were caused by past-dated test data.

---

## 🐛 Defects Found, Fixed & Closed

All defects were logged in Jira with full reproduction steps, severity/priority triage, linked requirements, verified via retesting, and released under `v1.1`:

| Defect ID | Summary | Severity | Priority | Status | Automated Regression Test |
|---|---|---|---|---|---|
| **CQA-1** | Replaying a booking POST on a full slot that the patient already booked displayed a misleading *"slot is fully booked"* error instead of *"You already have a booking for this slot."* | Medium | High | **Closed** | `test_cqa1_duplicate_booking_of_own_full_slot_says_already_booked` |
| **CQA-2** | Admin dashboard omitted existing allocated slots per doctor, displaying only an "Add Slot" action. | Medium | Medium | **Closed** | `test_cqa2_admin_dashboard_lists_slots_and_who_booked` |
| **CQA-3** | UI redesign regression caused doctor names to display with a duplicated prefix (`Dr. Dr. <Name>`). | Low | Low | **Closed** | `test_cqa3_doctor_name_has_no_duplicated_prefix` |

---

## 🤖 Automated UI Testing Suite (`ui_tests`)

Following the manual STLC closure, a comprehensive UI test automation suite was developed using **Selenium WebDriver + pytest** and the **Page Object Model (POM)** pattern.

### Framework Features:
- **Page Object Model (POM):** Clean separation of element locators and page interactions (`pages/`) from test assertions (`tests/`).
- **Resilient Locators:** Targeted testing using dedicated `data-qa` and `data-testid` attributes.
- **Test Isolation:** Tests create fresh patient accounts and slots when needed via helper flows (`flows.py`); seeded accounts are used for role-login scenarios.
- **Explicit Synchronization:** Robust explicit waits (`WebDriverWait`) replacing flaky hardcoded sleeps.
- **Automatic Failure Artifacts:** A browser screenshot is saved to `ui_tests/screenshots/` when a test call fails.
- **Headless & CI-Ready:** Supports both local visible browser execution and headless execution (`HEADLESS=1`).

### Test Coverage (39 Test Cases Collected):
- **Authentication (`test_auth.py`):** 10 tests covering valid logins for all 3 roles, incorrect password, unregistered email, HTML5 client validation, user registration, duplicate email rejection, and logout session termination.
- **Role & Access Boundaries (`test_roles.py`):** 9 tests verifying unauthorized route access restrictions (e.g., patient attempting to open `/admin/dashboard`, doctor accessing patient routes, unauthenticated visitors).
- **Patient Booking (`test_patient_booking.py`):** 10 tests covering specialization filtering, empty search states, single/multi-slot booking, slot capacity release on cancellation, re-booking after cancellation, full slot locking, duplicate booking prevention, past slot hiding, and **CQA-1 regression**.
- **Doctor Workflow (`test_doctor.py`):** 3 tests covering appointment visibility, marking appointments complete, doctor-patient schedule boundary enforcement, and **CQA-3 regression**.
- **Admin Workflow (`test_admin.py`):** 4 tests covering doctor account creation, duplicate email rejection, slot allocation, who-booked visibility, **CQA-2 regression**, and strict xfail on time format validation.
- **Prescription Upload (`test_prescription.py`):** 3 tests covering valid `.pdf` upload, rejection of unsupported file formats (`.txt`), and disabled upload for cancelled appointments.

---

## 📁 Repository Structure

```
clinic-app/
├── .github/                             # Continuous Integration Workflows
│   └── workflows/
│       └── ui-tests.yml                 # GitHub Actions pipeline (headless Chrome, pytest)
├── app/                                 # Flask Application Source Code
│   ├── __init__.py                      # Application factory & blueprint registration
│   ├── models.py                        # SQLAlchemy models (User, DoctorProfile, Slot, Appointment)
│   ├── routes/                          # Modular blueprint controllers
│   │   ├── admin.py                     # Doctor creation, slot allocation & dashboard
│   │   ├── api.py                       # REST API endpoints (auth, doctors, slots, appointments)
│   │   ├── auth.py                      # Authentication & session management
│   │   ├── doctor.py                    # Doctor schedule & status updates
│   │   └── patient.py                   # Search, booking, cancellation & prescription upload
│   ├── static/                          # Application CSS and client assets
│   └── templates/                       # Jinja2 HTML templates with data-qa attributes
├── docs/                                # QA reports, test cases, and RTM
│   ├── QA_Test_Cases_and_RTM.xlsx       # 41 manual test cases + live RTM + defect mappings
│   ├── Test_Closure_Report.docx         # Formal STLC closure report & automation addendum
│   └── Test_Strategy_and_Test_Plan.docx # Legacy e-commerce test plan (not clinic-specific)
├── ui_tests/                            # Selenium WebDriver + pytest Automation Suite
│   ├── pages/                           # Page Object Model classes
│   │   ├── admin_pages.py               # Admin dashboard & slot creation page objects
│   │   ├── auth_pages.py                # Login & registration page objects
│   │   ├── base_page.py                 # Common BasePage with wait helpers and locator methods
│   │   ├── doctor_pages.py              # Doctor dashboard page objects
│   │   └── patient_pages.py             # Patient search, doctor details & dashboard page objects
│   ├── tests/                           # Pytest automated test specifications
│   │   ├── test_admin.py                # Admin management & CQA-2 regression
│   │   ├── test_auth.py                 # Multi-role authentication & validation tests
│   │   ├── test_doctor.py               # Doctor workflows, boundaries & CQA-3 regression
│   │   ├── test_patient_booking.py      # Booking engine, capacity & CQA-1 regression
│   │   ├── test_prescription.py         # Prescription file upload & MIME validation
│   │   └── test_roles.py                # Role-based access control (RBAC) tests
│   ├── screenshots/                     # Automated failure screenshot storage
│   ├── config.py                        # Test URLs, default credentials & timeout parameters
│   ├── conftest.py                      # Pytest fixtures (WebDriver lifecycle, screenshot hooks)
│   ├── flows.py                         # Reusable business flows (dynamic registration, slot setup)
│   ├── pytest.ini                       # Pytest configuration & markers
│   ├── README.md                        # UI test execution instructions
│   └── requirements.txt                 # UI test dependencies (pytest, selenium)
├── uploads/                             # Prescription file upload storage directory
├── clinic.db                            # SQLite database instance
├── inspect_db.py                        # Diagnostic utility: inspect raw Slot records
├── inspect_users.py                     # Diagnostic utility: inspect raw User records
├── seed_data.py                         # Test database seeder with sample doctors & slots
├── run.py                               # Application entry point
├── requirements.txt                     # Application dependencies
├── .gitignore                           # Git ignore rules for Python bytecode and test artifacts
└── README.md                            # Comprehensive project overview
```

---

## 🛠️ Tools & Technologies Used

| Category | Tools & Libraries |
|---|---|
| **Application Under Test** | Python (CI: 3.12), Flask, Flask-SQLAlchemy, Flask-Login, SQLite, Jinja2, HTML5/CSS3 |
| **Test Automation** | pytest (>=7.0), Selenium WebDriver (>=4.20), Page Object Model (POM), Chrome WebDriver |
| **Continuous Integration (CI)** | GitHub Actions (automated headless test runs, failure artifact capture) |
| **Test Management** | Jira Cloud (Scrum Space, Epics, Tasks, Bug Tracking, Release Management, Labels) |
| **QA Documentation** | Microsoft Word (Test Strategy, Test Plan, Closure Report), Microsoft Excel (RTM & Test Repository) |
| **Diagnostics & API** | Chrome DevTools (DOM, Network, Console), Python SQLite Inspection Scripts, REST JSON API |

---

## ⚙️ Setup & Execution Guide

### 1. Prerequisites
- Python installed (the CI workflow uses Python 3.12)
- Google Chrome browser installed

### 2. Set Up and Run the Clinic Application
```bash
# Clone the repository
git clone https://github.com/AKHIL572/clinic-appointment-booking-qa.git
cd clinic-appointment-booking-qa

# Install application dependencies
pip install -r requirements.txt

# WARNING: drops and recreates all tables/data in clinic.db
python seed_data.py

# Start the Flask web server
python run.py
```
The application will be live at `http://127.0.0.1:5000`.

### 3. Seeded Test Credentials

| Role | Email | Password |
|---|---|---|
| **Admin** | `admin@clinic.test` | `AdminPass123` |
| **Doctor (Anjali Menon)** | `anjali@clinic.test` | `DoctorPass123` |
| **Doctor (Rahul Nair)** | `rahul@clinic.test` | `DoctorPass123` |
| **Patient** | `patient@clinic.test` | `PatientPass123` |

---

### 4. Running the UI Test Automation Suite

Open a separate terminal while the application is running:

```bash
# Navigate to the test suite directory
cd ui_tests

# Install test dependencies
pip install -r requirements.txt

# Run all 39 automated tests with visible browser
python -m pytest

# Run headless (recommended for CI pipelines)
# Windows PowerShell:
$env:HEADLESS="1"; python -m pytest
# macOS / Linux:
HEADLESS=1 python -m pytest

# Run only the defect regression suite (CQA-1, CQA-2, CQA-3)
python -m pytest -k cqa

# Run a specific test module (e.g., patient booking)
python -m pytest tests/test_patient_booking.py
```

Failed tests save a screenshot to `ui_tests/screenshots/`. Re-run `python seed_data.py` to reset the database between runs if needed; this deletes and recreates all database data.

Latest documented run (16 October 2026, per the closure-report addendum): **38 passed, 1 expected failure (xfail)**. The suite currently collects 39 tests; run it locally to verify the current state.

---

### 5. Continuous Integration (GitHub Actions)

A GitHub Actions workflow ([`.github/workflows/ui-tests.yml`](.github/workflows/ui-tests.yml)) automatically executes on every `push` and `pull_request` to `main`:
1. Launches an Ubuntu virtual environment with Python 3.12.
2. Installs requirements and seeds the SQLite database (`python seed_data.py`).
3. Starts the Flask server in the background and waits for availability.
4. Executes all 39 Selenium tests in headless mode (`HEADLESS=1 python -m pytest -v`).
5. Captures and uploads test failure screenshots as workflow run artifacts if any test fails. The workflow can also be started manually with `workflow_dispatch`.

---

## 🔍 Known Limitations & Continuous Improvement

1. **Slot Time Input Validation:** Slot creation start/end time fields currently accept free-text without standard time format (`HH:MM`) enforcement. Identified and documented in the Test Closure Report; automated with a strict `@pytest.mark.xfail` test (`test_slot_with_invalid_time_format_is_rejected`) to catch the fix once implemented.
2. **Notifications:** SMS and email notifications are not implemented.

---

## 👤 Author & QA Analyst

- **Author:** Akhil T V  
- **Email:** akhilhotttekkat135@gmail.com  
- **GitHub:** [@AKHIL572](https://github.com/AKHIL572)  
