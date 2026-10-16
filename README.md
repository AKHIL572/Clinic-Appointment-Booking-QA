# Clinic Appointment Booking System

**An End-to-End QA Project: Manual, API and UI Automation Testing**

**Status:** ✅ Completed (QA cycle closed, v1.0 → v1.1), with UI automation suite added afterwards
**Role:** QA Analyst (also built the application under test)
**Type:** Manual + API Testing, UI Automation (Selenium), Defect Lifecycle Management, Agile QA Process

---

## Purpose

This project demonstrates a complete, independent Software Testing Life Cycle (STLC) on a real, purpose-built application, not a public demo site, so that every requirement, test case, defect, and fix reflects genuine hands-on QA work.

## Goal / Objective

- Design and execute a full manual + API test cycle across a multi-role application (Patient / Doctor / Admin)
- Practice Agile QA workflow using Jira: Epics, Tasks, Bugs, Releases
- Find genuine defects through exploratory and structured testing, and carry each through a full defect lifecycle (Open → Fixed → Retest → Closed)
- Produce professional QA documentation: Test Strategy, Test Plan, RTM, Test Case Repository, Test Closure Report
- Automate the UI regression suite with Selenium WebDriver and pytest using the Page Object Model

## Problem Statement

Clinics need a system for patients to discover doctors by specialization, view available appointment slots, and book or cancel appointments, while doctors need visibility into their schedules, and admins need to onboard doctors and manage slot availability. This mirrors the domain of a prior Business Analyst project (BRD/SRS for an Ayurvedic clinic), giving continuity between requirements-gathering and hands-on QA work.

## Application Features

**Patient**
- Register and log in
- Search doctors by specialization
- View a doctor's available appointment slots
- Book and cancel appointments
- Upload a prescription file (PDF/JPG/PNG) against an appointment

**Doctor**
- View assigned appointments
- Mark an appointment as complete

**Admin**
- Create new doctor profiles
- Allocate appointment slots (date, time, capacity) per doctor
- View all doctors, their slots, and all system-wide appointments

**REST API**
- All core actions (register, login, search, book, cancel) available as JSON endpoints with correct status codes, independently testable via Postman/curl

## What Was Tested

### Manual and API testing (QA cycle v1.0 → v1.1)
- Exploratory, black-box functional testing across all modules by hand, before formal test case design
- 41 formal manual/API test cases designed and executed, tracked in a Requirement Traceability Matrix (RTM) with live formulas
- Authentication: valid/invalid login, weak passwords, duplicate emails, role-based redirection, logout/session handling
- Booking logic: valid booking, full-capacity slots, past-date slots, duplicate bookings by the same patient, cancellation, and re-booking after cancellation
- Doctor dashboard: appointment visibility, marking appointments complete
- Admin panel: doctor creation, slot allocation, duplicate-email handling
- REST API: status codes and validation across register/login/list/book/cancel endpoints, plus role-boundary enforcement (a patient cannot reach admin-only routes)
- Two suspected issues were investigated and ruled out using direct evidence (browser DevTools DOM inspection and a custom database-inspection script) rather than being assumed to be defects
- 3 genuine defects were found, root-caused, fixed, retested, and formally closed
- A post-redesign regression check caught a real regression (duplicated "Dr." title) before closure

**Explicitly not covered:** payment processing, performance/load testing, security/penetration testing, and email/SMS notifications (mocked out).

### UI automation (Selenium)
- 39 automated UI tests (38 pass, 1 expected failure documenting a known limitation)
- Authentication: role-based landing pages, invalid login, empty form, duplicate email, short password, logout
- Role boundaries: all six cross-role page combinations return "Forbidden", anonymous users are blocked
- Patient booking: search by specialization, book, cancel, re-book after cancel, full slot, duplicate booking, past slots hidden
- Doctor: sees only their own patients, marks an appointment complete
- Admin: add doctor, duplicate doctor email, slot and bookings visible on the dashboard
- Prescription upload: valid PDF accepted, unsupported file type rejected, no upload option on cancelled appointments
- One regression test per closed defect (CQA-1, CQA-2, CQA-3)

## Methodology

1. Built the application (Flask + SQLite) with three roles, modeled on a real clinic-booking domain
2. Authored the Test Strategy & Test Plan (scope, approach, entry/exit criteria, defect severity/priority matrix, risks)
3. Set up Jira (Scrum-template Space), including Releases (v1.0 Baseline, v1.1 Post-Redesign Fixes) and Labels (in place of Components, which team-managed Spaces don't support)
4. Created 5 Epics: Authentication, Slot Booking, Doctor Dashboard, Admin Panel, API Layer
5. Created 3 Tasks per Epic (Design test cases, Set up test environment, Execute test cases), 15 Tasks total
6. Performed exploratory black-box functional testing across all modules
7. Designed 41 formal test cases and built the RTM
8. Found and logged 3 genuine defects in Jira, each with steps to reproduce, severity, and priority
9. Investigated two suspected issues and ruled them out with direct evidence, documenting the reasoning rather than filing false tickets
10. Fixed all 3 confirmed defects, retested each, and closed the tickets
11. Released v1.1 in Jira once all linked defects were verified closed
12. Authored the Test Closure Report, evaluating exit criteria honestly, including what was *not* fully completed
13. Automated the UI regression suite with Selenium + pytest (Page Object Model) and ran it against the application

## Defects Found, Fixed, and Closed

| Defect ID | Summary | Severity | Status |
|---|---|---|---|
| CQA-1 | Duplicate booking attempt on a full-capacity slot returned a misleading "slot is fully booked" error instead of "you already have a booking" | Medium | Closed |
| CQA-2 | Admin dashboard did not display existing slots per doctor, only a link to add new ones | Medium | Closed |
| CQA-3 | Doctor name displayed with a duplicated "Dr." prefix after a UI redesign (regression) | Low | Closed |

### Issues found while building the automation (fixed)
- Prescription upload had a backend route but no upload control on the patient dashboard, so the feature could not be used from the UI. An upload form was added.
- The appointments empty state read "Cart is empty!" (leftover wording from a shopping-site demo). It now reads "No appointments yet."

## Project Structure

```
clinic-app/
├── README.md                      # This file
├── run.py                         # Flask entry point
├── seed_data.py                   # Seeds admin/doctor/patient test accounts + sample slots
├── requirements.txt
├── app/
│   ├── __init__.py                 # App factory, blueprint registration
│   ├── models.py                   # User, DoctorProfile, Slot, Appointment (SQLAlchemy)
│   ├── routes/
│   │   ├── auth.py                 # Register, login, logout
│   │   ├── patient.py              # Search, book, cancel, upload prescription
│   │   ├── doctor.py               # View schedule, mark appointment complete
│   │   ├── admin.py                # Add doctor, add slot, view dashboards
│   │   └── api.py                  # JSON REST API mirroring the UI actions
│   └── templates/                  # Jinja2 HTML templates (one per page/role)
├── ui_tests/                       # Selenium UI automation suite
│   ├── config.py                   # Base URL, timeouts, seeded accounts
│   ├── conftest.py                 # Browser fixture, new-patient fixture, failure screenshots
│   ├── flows.py                    # Reusable multi-step actions (login, book, create slot)
│   ├── pages/                      # Page Objects (locators + actions, no assertions)
│   └── tests/                      # auth, roles, patient booking, doctor, admin, prescription
├── inspect_db.py                   # Diagnostic script: dumps raw Slot table
├── inspect_users.py                # Diagnostic script: dumps raw User table
└── docs/                           # All QA documentation deliverables
    ├── Test_Strategy_and_Test_Plan.docx
    ├── QA_Test_Cases_and_RTM.xlsx    # 41 test cases + RTM + Defect ID cross-references
    └── Test_Closure_Report.docx
```

**Note on defect tracking:** there is no separate "defect log" file. All 3 defects (CQA-1, CQA-2, CQA-3) are tracked as the source of truth in **Jira**, and cross-referenced in the `Defect ID` column of `QA_Test_Cases_and_RTM.xlsx` and summarized in `Test_Closure_Report.docx`. See Jira Workflow Evidence below for screenshots of the actual tickets.

## Tools and Technologies Used

| Category | Tools |
|---|---|
| Application | Python, Flask, Flask-SQLAlchemy, Flask-Login, SQLite, Jinja2, HTML/CSS |
| Test Management | Jira Cloud (Scrum Space, Epics/Tasks/Bugs, Releases, Labels) |
| Test Documentation | Microsoft Word (Test Strategy & Plan, Test Closure Report), Excel (RTM + Test Case Repository, formula-driven) |
| API Testing | Postman collection with scripted assertions, Newman (CLI runner) |
| UI Automation | Selenium WebDriver (Python), pytest, Page Object Model, explicit waits, fixtures |
| Debugging / Diagnostics | Browser DevTools (DOM inspection), custom Python scripts for direct database inspection |

## Deliverables Produced

- [Test Strategy & Test Plan](docs/Test_Strategy_and_Test_Plan.docx)
- [Requirement Traceability Matrix + 41 Test Cases](docs/QA_Test_Cases_and_RTM.xlsx) (Excel, formula-driven)
- Jira project: 5 Epics, 15 Tasks, 3 Bugs (all closed), 2 Releases
- [Test Closure Report](docs/Test_Closure_Report.docx)
- Selenium UI automation suite (`ui_tests/`, 39 tests)
- The application itself (this repository)

## Jira Workflow Evidence

_Screenshots below. Since the Jira site itself is private, these serve as proof of the workflow instead of a live link._

- **Backlog/Board:** all 5 Epics with 15 Tasks nested, marked Done
  `![Board](docs/screenshots/board.png)`
- **Sample Bug ticket (CQA-1):** description, severity, steps to reproduce, status
  `![Bug CQA-1](docs/screenshots/cqa-1.png)`
- **Releases page:** v1.0 and v1.1, both marked Released
  `![Releases](docs/screenshots/releases.png)`

## Key Skills Demonstrated

- STLC / Agile QA process ownership from requirement analysis through closure
- Manual black-box and exploratory testing
- Test case design, RTM construction, defect severity/priority triage
- Defect lifecycle management in Jira (Open → Fixed → Retest → Closed)
- API testing with status-code-level assertions
- UI test automation with Selenium WebDriver and pytest: Page Object Model, explicit waits, fixtures, independent self-contained tests, failure screenshots
- Automated regression tests for closed defects
- Root-cause investigation using DevTools and direct database inspection, distinguishing genuine defects from environmental/data issues
- Professional QA documentation aligned to real-world formats

## Known Limitations

- Slot creation time fields lack format validation (no AM/PM, no HH:MM enforcement). It is documented and covered by an expected-failure (`xfail`) automated test, and not fixed this cycle.
- The UI suite takes about 5 minutes for 39 tests because every test sets up its own data through the browser.
- Not yet implemented: CI pipeline (GitHub Actions), Allure reporting, and a BDD (Gherkin) layer.
- The REST API is covered by Postman/Newman only, not by the Selenium suite.

## Setup

```bash
pip install -r requirements.txt
python seed_data.py     # creates clinic.db with sample doctors/slots
python run.py           # serves on http://127.0.0.1:5000
```

## Running the UI automation

With the app running (second terminal):

```bash
cd ui_tests
pip install -r requirements.txt
python -m pytest                 # visible Chrome window
python -m pytest -k cqa          # only the defect regression tests
HEADLESS=1 python -m pytest      # no browser window
```

Failed tests save a screenshot to `ui_tests/screenshots/`. Re-run `python seed_data.py` to reset the database between runs if needed.

Latest run: **38 passed, 1 expected failure (xfail)** in about 4 minutes 49 seconds.

## Seeded test accounts

| Role    | Email                  | Password        |
|---------|-------------------------|------------------|
| Admin   | admin@clinic.test       | AdminPass123     |
| Doctor  | anjali@clinic.test      | DoctorPass123    |
| Patient | patient@clinic.test     | PatientPass123   |

---

*Prepared by Akhil T V, QA Analyst*
