"""
Unit tests for the Fitbook API.

This suite verifies booking functionality, including:
- Successful bookings
- Input validation
- Overbooking prevention
- Handling invalid class IDs
- Duplicate booking protection
"""

import unittest
from app import app, db
from models import FitnessClass
from datetime import datetime, timedelta
import pytz

class BookingAPITestCase(unittest.TestCase):
    """Test case for /book endpoint and booking logic."""

    def setUp(self):
        """Set up test environment: clean DB and create a sample fitness class."""
        self.app = app.test_client()
        self.ist = pytz.timezone('Asia/Kolkata')

        with app.app_context():
            db.drop_all()
            db.create_all()
            # Add one test class with 2 available slots
            test_class = FitnessClass(
                name="Test Yoga",
                instructor="Test Instructor",
                datetime_ist=self.ist.localize(datetime.now() + timedelta(days=1)),
                available_slots=2
            )
            db.session.add(test_class)
            db.session.commit()
            self.class_id = test_class.id

    def test_successful_booking(self):
        """Should return 201 Created when booking is successful."""
        response = self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Alice",
            "client_email": "alice@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Booking successful", response.data)

    def test_missing_fields(self):
        """Should return 400 Bad Request if required fields are missing."""
        response = self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Bob"  # Missing email
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing fields", response.data)

    def test_overbooking(self):
        """Should return 400 when trying to book more than available slots."""
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
        # Try third booking (should fail)
        response = self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Eve",
            "client_email": "eve@example.com"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"No slots available", response.data)

    def test_invalid_class(self):
        """Should return 404 if class_id is invalid."""
        response = self.app.post("/book", json={
            "class_id": 9999,
            "client_name": "Foo",
            "client_email": "foo@example.com"
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Class not found", response.data)

    def test_duplicate_booking(self):
        """Should return 409 Conflict if booking is already made for same class and email."""
        # First booking
        response1 = self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Grace",
            "client_email": "grace@example.com"
        })
        self.assertEqual(response1.status_code, 201)

        # Second (duplicate) booking
        response2 = self.app.post("/book", json={
            "class_id": self.class_id,
            "client_name": "Grace",
            "client_email": "grace@example.com"
        })
        self.assertEqual(response2.status_code, 409)
        self.assertIn(b"already booked", response2.data)


if __name__ == "__main__":
    unittest.main()
