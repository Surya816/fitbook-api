# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import pytz
import logging

from models import db, FitnessClass, Booking

app = Flask(__name__)
CORS(app)

# Configure SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
IST = pytz.timezone('Asia/Kolkata')

# DB setup
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/classes", methods=["GET"])
def get_classes():
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
    data = request.get_json()
    class_id = data.get("class_id")
    client_name = data.get("client_name")
    client_email = data.get("client_email")

    if not all([class_id, client_name, client_email]):
        return jsonify({"error": "Missing fields"}), 400

    cls = FitnessClass.query.get(class_id)
    if not cls:
        return jsonify({"error": "Class not found"}), 404

    if cls.available_slots <= 0:
        return jsonify({"error": "No slots available"}), 400

    # ✅ Check for duplicate booking
    existing_booking = Booking.query.filter_by(
        class_id=class_id, client_email=client_email
    ).first()

    if existing_booking:
        return jsonify({"error": "You have already booked this class."}), 409  # Conflict

    # Create booking
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
    app.run(debug=True)
