"""
Database models for the Fitbook API.

This module defines two SQLAlchemy models:
- FitnessClass: represents a fitness class that users can book
- Booking: represents a user's booking for a fitness class
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class FitnessClass(db.Model):
    """
    Model representing a fitness class (e.g., Yoga, Zumba, HIIT).

    Attributes:
        id (int): Primary key
        name (str): Name of the class
        instructor (str): Name of the instructor
        datetime_ist (datetime): Scheduled date and time in IST
        available_slots (int): Number of available booking slots
    """
    __tablename__ = 'fitness_class'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    instructor = db.Column(db.String(80), nullable=False)
    datetime_ist = db.Column(db.DateTime, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)


class Booking(db.Model):
    """
    Model representing a booking for a fitness class.

    Attributes:
        id (int): Primary key
        class_id (int): Foreign key referencing FitnessClass.id
        client_name (str): Name of the client
        client_email (str): Email of the client
        timestamp (datetime): Time when the booking was made
    """
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('fitness_class.id'), nullable=False)
    client_name = db.Column(db.String(80), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
