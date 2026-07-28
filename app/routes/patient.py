import os
from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import db, DoctorProfile, Slot, Appointment

patient_bp = Blueprint("patient", __name__, url_prefix="/patient")

ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}


def _require_patient():
    return current_user.is_authenticated and current_user.role == "patient"


@patient_bp.route("/dashboard")
@login_required
def dashboard():
    if not _require_patient():
        return "Forbidden: patient access only", 403

    specialization = request.args.get("specialization", "").strip()
    query = DoctorProfile.query
    if specialization:
        query = query.filter(DoctorProfile.specialization.ilike(f"%{specialization}%"))
    doctors = query.all()

    my_appointments = Appointment.query.filter_by(patient_id=current_user.id).all()

    return render_template("patient_dashboard.html", doctors=doctors, appointments=my_appointments)


@patient_bp.route("/doctor/<int:doctor_id>")
@login_required
def doctor_detail(doctor_id):
    if not _require_patient():
        return "Forbidden: patient access only", 403

    doctor = DoctorProfile.query.get_or_404(doctor_id)
    upcoming_slots = [s for s in doctor.slots if not s.is_past()]
    return render_template("doctor_detail.html", doctor=doctor, slots=upcoming_slots)


@patient_bp.route("/book/<int:slot_id>", methods=["POST"])
@login_required
def book(slot_id):
    if not _require_patient():
        return "Forbidden: patient access only", 403

    slot = Slot.query.get_or_404(slot_id)

    # --- Business rule validations (the actual QA surface of this app) ---
    if slot.is_past():
        flash("Cannot book a slot in the past.", "error")
        return redirect(url_for("patient.doctor_detail", doctor_id=slot.doctor_id))

    # Check for user's own existing booking BEFORE the capacity check,
    # so they see "you already booked this" instead of the misleading
    # "slot is fully booked" when their own booking filled the last seat.
    existing = Appointment.query.filter_by(
        patient_id=current_user.id, slot_id=slot.id
    ).filter(Appointment.status.in_(["requested", "confirmed"])).first()
    if existing:
        flash("You already have a booking for this slot.", "error")
        return redirect(url_for("patient.doctor_detail", doctor_id=slot.doctor_id))

    if slot.is_full():
        flash("This slot is already fully booked.", "error")
        return redirect(url_for("patient.doctor_detail", doctor_id=slot.doctor_id))

    appointment = Appointment(patient_id=current_user.id, slot_id=slot.id, status="confirmed")
    slot.booked_count += 1
    db.session.add(appointment)
    db.session.commit()

    flash("Appointment booked successfully.", "success")
    return redirect(url_for("patient.dashboard"))


@patient_bp.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
@login_required
def cancel(appointment_id):
    if not _require_patient():
        return "Forbidden: patient access only", 403

    appt = Appointment.query.get_or_404(appointment_id)
    if appt.patient_id != current_user.id:
        return "Forbidden: not your appointment", 403

    if appt.status == "completed":
        flash("Cannot cancel a completed appointment.", "error")
        return redirect(url_for("patient.dashboard"))

    if appt.status != "cancelled":
        appt.status = "cancelled"
        appt.slot.booked_count = max(0, appt.slot.booked_count - 1)
        db.session.commit()
        flash("Appointment cancelled.", "success")

    return redirect(url_for("patient.dashboard"))


@patient_bp.route("/appointments/<int:appointment_id>/upload", methods=["POST"])
@login_required
def upload_prescription(appointment_id):
    if not _require_patient():
        return "Forbidden: patient access only", 403

    appt = Appointment.query.get_or_404(appointment_id)
    if appt.patient_id != current_user.id:
        return "Forbidden: not your appointment", 403

    file = request.files.get("prescription")
    if not file or file.filename == "":
        flash("No file selected.", "error")
        return redirect(url_for("patient.dashboard"))

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        flash("Unsupported file type. Allowed: pdf, jpg, jpeg, png.", "error")
        return redirect(url_for("patient.dashboard"))

    filename = secure_filename(f"appt_{appointment_id}_{file.filename}")
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    appt.prescription_filename = filename
    db.session.commit()

    flash("Prescription uploaded.", "success")
    return redirect(url_for("patient.dashboard"))
