"""
Prints every User's name exactly as stored in the database — no
template rendering involved. Settles whether "Dr. Dr." is coming from
the stored data itself or from something in the display layer.

Run with: python inspect_users.py
"""
from app import create_app
from app.models import db, User

app = create_app()

with app.app_context():
    users = User.query.order_by(User.id).all()
    print(f"{'ID':<4}{'Role':<10}{'Name (raw, repr)'}")
    print("-" * 60)
    for u in users:
        print(f"{u.id:<4}{u.role:<10}{u.name!r}")