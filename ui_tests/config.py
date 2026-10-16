"""Central settings + the seeded accounts created by seed_data.py."""
import os

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")
HEADLESS = os.getenv("HEADLESS", "0") == "1"   # HEADLESS=1 -> no browser window (needed for CI)
TIMEOUT = 10                                   # seconds for every explicit wait

PATIENT = {"name": "Test Patient", "email": "patient@clinic.test",
           "password": "PatientPass123", "path": "/patient/dashboard"}
DOCTOR = {"name": "Dr. Anjali Menon", "email": "anjali@clinic.test",
          "password": "DoctorPass123", "path": "/doctor/dashboard"}
DOCTOR2 = {"name": "Dr. Rahul Nair", "email": "rahul@clinic.test",
           "password": "DoctorPass123", "path": "/doctor/dashboard"}
ADMIN = {"name": "Admin User", "email": "admin@clinic.test",
         "password": "AdminPass123", "path": "/admin/dashboard"}

DOCTOR_NAME = DOCTOR["name"]
