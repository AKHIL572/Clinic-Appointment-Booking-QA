from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, User, DoctorProfile, Slot, Appointment

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _require_admin():
    return current_user.is_authenticated and current_user.role == "admin"


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if not _require_admin():
        return "Forbidden: admin access only", 403

    doctors = DoctorProfile.query.all()
    appointments = Appointment.query.all()
    slots = Slot.query.order_by(Slot.slot_date).all()
    return render_template("admin_dashboard.html", doctors=doctors, appointments=appointments, slots=slots)


@admin_bp.route("/doctors/new", methods=["GET", "POST"])
@login_required
def new_doctor():
    if not _require_admin():
        return "Forbidden: admin access only", 403

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        specialization = request.form.get("specialization", "").strip()
        password = request.form.get("password", "")

        if not all([name, email, specialization, password]):
            flash("All fields are required.", "error")
            return render_template("new_doctor.html")

        if User.query.filter_by(email=email).first():
            flash("A user with this email already exists.", "error")
            return render_template("new_doctor.html")

        user = User(name=name, email=email, role="doctor")
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # get user.id before commit

        profile = DoctorProfile(user_id=user.id, specialization=specialization)
        db.session.add(profile)
        db.session.commit()

        flash("Doctor created.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("new_doctor.html")


@admin_bp.route("/doctors/<int:doctor_id>/slots/new", methods=["GET", "POST"])
@login_required
def new_slot(doctor_id):
    if not _require_admin():
        return "Forbidden: admin access only", 403

    doctor = DoctorProfile.query.get_or_404(doctor_id)

    if request.method == "POST":
        slot_date_raw = request.form.get("slot_date", "")
        start_time = request.form.get("start_time", "")
        end_time = request.form.get("end_time", "")
        capacity = request.form.get("capacity", "1")

        try:
            slot_date = datetime.strptime(slot_date_raw, "%Y-%m-%d").date()
            capacity = int(capacity)
        except ValueError:
            flash("Invalid date or capacity value.", "error")
            return render_template("new_slot.html", doctor=doctor)

        if capacity < 1:
            flash("Capacity must be at least 1.", "error")
            return render_template("new_slot.html", doctor=doctor)

        slot = Slot(
            doctor_id=doctor.id,
            slot_date=slot_date,
            start_time=start_time,
            end_time=end_time,
            capacity=capacity,
        )
        db.session.add(slot)
        db.session.commit()
        flash("Slot added.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("new_slot.html", doctor=doctor)
