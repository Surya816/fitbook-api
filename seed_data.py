"""
Seed script to populate the database with sample fitness classes
(Yoga, Zumba, HIIT) in IST timezone. Run this before launching the app.
"""

from app import app
from models import db, FitnessClass
from datetime import datetime, timedelta
import pytz

# Activate Flask app context to allow DB operations
with app.app_context():
    db.create_all()

    # Set IST timezone for consistency
    ist = pytz.timezone('Asia/Kolkata')

    # Sample class data for seeding
    sample_classes = [
        FitnessClass(
            name="Yoga",
            instructor="Aarav Mehta",
            datetime_ist=ist.localize(datetime.now() + timedelta(days=1, hours=6)),
            available_slots=1
        ),
        FitnessClass(
            name="Zumba",
            instructor="Maya Rao",
            datetime_ist=ist.localize(datetime.now() + timedelta(days=1, hours=9)),
            available_slots=8
        ),
        FitnessClass(
            name="HIIT",
            instructor="Rahul Das",
            datetime_ist=ist.localize(datetime.now() + timedelta(days=2, hours=7)),
            available_slots=6
        )
    ]

    # Insert all classes into the database at once
    db.session.bulk_save_objects(sample_classes)
    db.session.commit()

    print("✅ Sample classes added.")
