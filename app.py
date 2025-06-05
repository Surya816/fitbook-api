"""
Fitbook API – Flask application for managing fitness class bookings.
Allows users to view classes, book a slot, and retrieve bookings by email.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import pytz
import logging

from models import db, FitnessClass, Booking

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Set up logging for activity tracking
logging.basicConfig(level=logging.INFO)

# Define IST timezone for class scheduling
IST = pytz.timezone('Asia/Kolkata')

# Initialize database tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """Serves the main HTML UI page."""
    return render_template("index.html")


@app.route("/classes", methods=["GET"])
def get_classes():
    """
    Returns a list of all upcoming fitness classes.
    Optional Query Param:
        ?date=YYYY-MM-DD - filters classes on that calendar day (IST)
    Output: JSON list with class ID, name, instructor, time (ISO), available slots.
    """
    date_str = request.args.get("date")
    ist = pytz.timezone('Asia/Kolkata')

    if date_str:
        try:
            # Parse input date and localize to IST
            start = ist.localize(datetime.strptime(date_str, "%Y-%m-%d"))
            end = start.replace(hour=23, minute=59, second=59)

            classes = FitnessClass.query.filter(
                FitnessClass.datetime_ist >= start,
                FitnessClass.datetime_ist <= end
            ).all()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    else:
        classes = FitnessClass.query.all()

    result = []
    for cls in classes:
        result.append({
            "id": cls.id,
            "name": cls.name,
            "instructor": cls.instructor,
            "datetime": cls.datetime_ist.isoformat(),
            "available_slots": cls.available_slots
        })

    return jsonify(result), 200



@app.route("/book", methods=["POST"])
def book_class():
    """
    Accepts a booking request (class_id, client_name, client_email).
    Validates:
      - Required fields are present
      - Class exists and has available slots
      - No duplicate booking by same email
    On success, creates booking and decrements available slot.
    """
    data = request.get_json()
    class_id = data.get("class_id")
    client_name = data.get("client_name")
    client_email = data.get("client_email")

    # Validate required fields
    if not all([class_id, client_name, client_email]):
        return jsonify({"error": "Missing fields"}), 400

    # Check if class exists
    cls = FitnessClass.query.get(class_id)
    if not cls:
        return jsonify({"error": "Class not found"}), 404

    # Check if slots are available
    if cls.available_slots <= 0:
        return jsonify({"error": "No slots available"}), 400

    # Prevent duplicate booking for same class by same email
    existing_booking = Booking.query.filter_by(
        class_id=class_id, client_email=client_email
    ).first()
    if existing_booking:
        return jsonify({"error": "You have already booked this class."}), 409

    # Create booking and update available slots
    booking = Booking(
        class_id=class_id,
        client_name=client_name,
        client_email=client_email
    )
    db.session.add(booking)
    cls.available_slots -= 1
    db.session.commit()

    logging.info(f"Booking created for {client_email} in class {class_id}")
    return jsonify({"message": "Booking successful"}), 201


@app.route("/bookings", methods=["GET"])
def get_bookings():
    """
    Returns all bookings made by a specific email.
    Requires: ?email=someone@example.com in the query string.
    Output: List of class info + client name/email for each booking.
    """
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email query param is required"}), 400

    bookings = Booking.query.filter_by(client_email=email).all()
    result = []
    for b in bookings:
        cls = FitnessClass.query.get(b.class_id)
        result.append({
            "class_name": cls.name,
            "instructor": cls.instructor,
            "datetime": cls.datetime_ist.isoformat(),
            "client_name": b.client_name,
            "client_email": b.client_email
        })

    return jsonify(result), 200


if __name__ == "__main__":
    # Run the Flask development server
    app.run(debug=True)
