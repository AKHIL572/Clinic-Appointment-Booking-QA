# UI automation for the Clinic Appointment Booking System

Selenium WebDriver + pytest + Page Object Model.

## Run

1. Start the app (from the project root): `python seed_data.py` then `python run.py`
2. In another terminal:
   ```
   cd ui_tests
   pip install -r requirements.txt
   pytest                    # visible Chrome
   HEADLESS=1 pytest         # no window (CI)      (Windows PowerShell: $env:HEADLESS=1; pytest)
   pytest -k cqa             # only the three defect regression tests
   ```
Screenshots of failed tests are saved to `screenshots/`.

## Layout
- `config.py`  URLs, timeouts, seeded accounts
- `pages/`     one class per page (locators + actions); no assertions
- `flows.py`   multi-step helpers (login, register patient, create slot, book)
- `tests/`     auth, roles, patient booking, doctor, admin (+ CQA-1/2/3 regressions)

Every test creates its own patient and slot, so tests are independent. Re-run
`python seed_data.py` any time to reset the database.
