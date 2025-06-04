from app import app
from models import db, FitnessClass
from datetime import datetime, timedelta
import pytz

with app.app_context():
    db.create_all()

    ist = pytz.timezone('Asia/Kolkata')

    sample_classes = [
        FitnessClass(
            name="Yoga",
            instructor="Aarav Mehta",
            datetime_ist=ist.localize(datetime.now() + timedelta(days=1, hours=6)),
            available_slots=10
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

    db.session.bulk_save_objects(sample_classes)
    db.session.commit()

    print("✅ Sample classes added.")
