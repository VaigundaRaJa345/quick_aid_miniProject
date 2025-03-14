import os

class Config:
    SECRET_KEY = 'your_secret_key'  # Change this to a strong random key
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Update as per your database
    SQLALCHEMY_TRACK_MODIFICATIONS = False