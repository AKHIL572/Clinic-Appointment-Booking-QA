"""
Seed the database with an admin, a couple of doctors, and some slots
so there's something real to test against immediately.
Run with: python seed_data.py
"""
from datetime import date, timedelta
from app import create_app
from app.models import db, User, DoctorProfile, Slot

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(name="Admin User", email="admin@clinic.test", role="admin")
    admin.set_password("AdminPass123")
    db.session.add(admin)

    doc1_user = User(name="Dr. Anjali Menon", email="anjali@clinic.test", role="doctor")
    doc1_user.set_password("DoctorPass123")
    db.session.add(doc1_user)
    db.session.flush()
    doc1 = DoctorProfile(user_id=doc1_user.id, specialization="Ayurveda", bio="15 years of Ayurvedic practice.")
    db.session.add(doc1)

    doc2_user = User(name="Dr. Rahul Nair", email="rahul@clinic.test", role="doctor")
    doc2_user.set_password("DoctorPass123")
    db.session.add(doc2_user)
    db.session.flush()
    doc2 = DoctorProfile(user_id=doc2_user.id, specialization="Dermatology", bio="Skin and hair specialist.")
    db.session.add(doc2)

    db.session.flush()

    tomorrow = date.today() + timedelta(days=1)
    next_week = date.today() + timedelta(days=7)
    yesterday = date.today() - timedelta(days=1)

    slots = [
        Slot(doctor_id=doc1.id, slot_date=tomorrow, start_time="09:00", end_time="09:30", capacity=1),
        Slot(doctor_id=doc1.id, slot_date=tomorrow, start_time="09:30", end_time="10:00", capacity=2),
        Slot(doctor_id=doc1.id, slot_date=next_week, start_time="10:00", end_time="10:30", capacity=1),
        Slot(doctor_id=doc1.id, slot_date=yesterday, start_time="09:00", end_time="09:30", capacity=1),  # past slot, for negative testing
        Slot(doctor_id=doc2.id, slot_date=tomorrow, start_time="11:00", end_time="11:30", capacity=1),
    ]
    db.session.add_all(slots)

    patient = User(name="Test Patient", email="patient@clinic.test", role="patient")
    patient.set_password("PatientPass123")
    db.session.add(patient)

    db.session.commit()
    print("Seed complete.")
    print("Admin login:   admin@clinic.test / AdminPass123")
    print("Doctor login:  anjali@clinic.test / DoctorPass123")
    print("Patient login: patient@clinic.test / PatientPass123")
