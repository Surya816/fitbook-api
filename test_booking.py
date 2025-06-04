import unittest
from app import app, db
from models import FitnessClass
from datetime import datetime, timedelta
import pytz

class BookingAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.ist = pytz.timezone('Asia/Kolkata')

        with app.app_context():
            db.drop_all()
            db.create_all()
            # Add one test class
            test_class = FitnessClass(
                name="Test Yoga",
                instructor="Test Instructor",
                datetime_ist=self.ist.localize(datetime.now() + timedelta(days=1)),
                available_slots=2  # allow 2 bookings
            )
            db.session.add(test_class)
            db.session.commit()
            self.class_id = test_class.id

    def test_successful_booking(self):
        response = self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Alice",
            "client_email": "alice@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Booking successful", response.data)

    def test_missing_fields(self):
        response = self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Bob"
            # Missing email
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing fields", response.data)

    def test_overbooking(self):
        # Fill all slots
        self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Charlie",
            "client_email": "charlie@example.com"
        })
        self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Dave",
            "client_email": "dave@example.com"
        })
        # Now try third booking
        response = self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Eve",
            "client_email": "eve@example.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"No slots available", response.data)

    def test_invalid_class(self):
        response = self.app.post("/book", json={
            "class_id": 9999,
            "client_name": "Foo",
            "client_email": "foo@example.com"
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Class not found", response.data)

    def test_duplicate_booking(self):
        # First booking
        response1 = self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Grace",
            "client_email": "grace@example.com"
        })
        self.assertEqual(response1.status_code, 201)

        # Duplicate booking for same class/email
        response2 = self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Grace",
            "client_email": "grace@example.com"
        })
        self.assertEqual(response2.status_code, 409)
        self.assertIn(b"already booked", response2.data)

if __name__ == "__main__":
    unittest.main()
