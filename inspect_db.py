"""
Diagnostic script — prints every Slot row exactly as stored in the
database, bypassing the UI entirely. Run this whenever the UI shows
something unexpected, to check whether the problem is in the data
or in how it's being displayed.

Run with: python inspect_db.py
"""
from app import create_app
from app.models import db, Slot, DoctorProfile

app = create_app()

with app.app_context():
    slots = Slot.query.order_by(Slot.id).all()
    print(f"{'ID':<4}{'Doctor':<20}{'Date':<12}{'Start':<8}{'End':<8}{'Capacity':<10}{'Booked'}")
    print("-" * 70)
    for s in slots:
        doctor_name = s.doctor.user.name if s.doctor else "UNKNOWN"
        print(f"{s.id:<4}{doctor_name:<20}{str(s.slot_date):<12}{s.start_time:<8}{s.end_time:<8}{s.capacity:<10}{s.booked_count}")