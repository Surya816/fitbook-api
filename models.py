# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FitnessClass(db.Model):
    __tablename__ = 'fitness_class'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    instructor = db.Column(db.String(80), nullable=False)
    datetime_ist = db.Column(db.DateTime, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('fitness_class.id'), nullable=False)
    client_name = db.Column(db.String(80), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
