from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, DoctorProfile, Appointment

doctor_bp = Blueprint("doctor", __name__, url_prefix="/doctor")


def _require_doctor():
    return current_user.is_authenticated and current_user.role == "doctor"


@doctor_bp.route("/dashboard")
@login_required
def dashboard():
    if not _require_doctor():
        return "Forbidden: doctor access only", 403

    profile = DoctorProfile.query.filter_by(user_id=current_user.id).first()
    appointments = []
    if profile:
        slot_ids = [s.id for s in profile.slots]
        appointments = Appointment.query.filter(Appointment.slot_id.in_(slot_ids)).all()

    return render_template("doctor_dashboard.html", profile=profile, appointments=appointments)


@doctor_bp.route("/appointments/<int:appointment_id>/complete", methods=["POST"])
@login_required
def complete(appointment_id):
    if not _require_doctor():
        return "Forbidden: doctor access only", 403

    appt = Appointment.query.get_or_404(appointment_id)
    profile = DoctorProfile.query.filter_by(user_id=current_user.id).first()

    if not profile or appt.slot.doctor_id != profile.id:
        return "Forbidden: not your appointment", 403

    if appt.status == "cancelled":
        flash("Cannot complete a cancelled appointment.", "error")
    else:
        appt.status = "completed"
        db.session.commit()
        flash("Appointment marked complete.", "success")

    return redirect(url_for("doctor.dashboard"))
