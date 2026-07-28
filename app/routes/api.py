from datetime import date
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, DoctorProfile, Slot, Appointment

api_bp = Blueprint("api", __name__)


@api_bp.route("/register", methods=["POST"])
def api_register():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "name, email, and password are required"}), 400
    if len(password) < 8:
        return jsonify({"error": "password must be at least 8 characters"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 409

    user = User(name=name, email=email, role="patient")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 201


@api_bp.route("/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "incorrect email or password"}), 401

    login_user(user)
    return jsonify({"id": user.id, "name": user.name, "role": user.role}), 200


@api_bp.route("/logout", methods=["POST"])
@login_required
def api_logout():
    logout_user()
    return "", 204


@api_bp.route("/doctors", methods=["GET"])
def api_doctors():
    specialization = request.args.get("specialization", "").strip()
    query = DoctorProfile.query
    if specialization:
        query = query.filter(DoctorProfile.specialization.ilike(f"%{specialization}%"))
    doctors = query.all()
    return jsonify([
        {"id": d.id, "name": d.user.name, "specialization": d.specialization}
        for d in doctors
    ])


@api_bp.route("/doctors/<int:doctor_id>/slots", methods=["GET"])
def api_doctor_slots(doctor_id):
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    slots = [s for s in doctor.slots if not s.is_past()]
    return jsonify([
        {
            "id": s.id, "date": s.slot_date.isoformat(), "start_time": s.start_time,
            "end_time": s.end_time, "capacity": s.capacity, "booked_count": s.booked_count,
            "is_full": s.is_full(),
        }
        for s in slots
    ])


@api_bp.route("/appointments", methods=["POST"])
@login_required
def api_book_appointment():
    if current_user.role != "patient":
        return jsonify({"error": "only patients can book appointments"}), 403

    data = request.get_json(silent=True) or {}
    slot_id = data.get("slot_id")
    slot = Slot.query.get(slot_id)
    if slot is None:
        return jsonify({"error": "slot not found"}), 404

    if slot.is_past():
        return jsonify({"error": "cannot book a slot in the past"}), 422

    # Check duplicate booking BEFORE capacity (see fix note in patient.py)
    existing = Appointment.query.filter_by(
        patient_id=current_user.id, slot_id=slot.id
    ).filter(Appointment.status.in_(["requested", "confirmed"])).first()
    if existing:
        return jsonify({"error": "already booked for this slot"}), 409

    if slot.is_full():
        return jsonify({"error": "slot is fully booked"}), 409

    appt = Appointment(patient_id=current_user.id, slot_id=slot.id, status="confirmed")
    slot.booked_count += 1
    db.session.add(appt)
    db.session.commit()
    return jsonify({"id": appt.id, "status": appt.status}), 201


@api_bp.route("/appointments", methods=["GET"])
@login_required
def api_my_appointments():
    appts = Appointment.query.filter_by(patient_id=current_user.id).all()
    return jsonify([{"id": a.id, "slot_id": a.slot_id, "status": a.status} for a in appts])


@api_bp.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
@login_required
def api_cancel_appointment(appointment_id):
    appt = Appointment.query.get_or_404(appointment_id)
    if appt.patient_id != current_user.id:
        return jsonify({"error": "not your appointment"}), 403
    if appt.status == "completed":
        return jsonify({"error": "cannot cancel a completed appointment"}), 422

    appt.status = "cancelled"
    appt.slot.booked_count = max(0, appt.slot.booked_count - 1)
    db.session.commit()
    return jsonify({"id": appt.id, "status": appt.status}), 200