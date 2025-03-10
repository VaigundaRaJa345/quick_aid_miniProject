from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class EmergencyDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False, unique=True)
    vehicle_number = db.Column(db.String(15), nullable=False, unique=True)
    blood_group = db.Column(db.String(5))
    allergies = db.Column(db.String(255))
    differently_abled = db.Column(db.String(255))
    alt_contact = db.Column(db.String(15))
    aztec_code = db.Column(db.String(255))