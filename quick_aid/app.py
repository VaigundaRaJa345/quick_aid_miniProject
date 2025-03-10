from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from extensions import db, bcrypt, login_manager  # Import extensions
from models import User, Details
from config import Config
import random
import string
import segno  # QR code generation
import os
from datetime import datetime

# ✅ Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# ✅ Initialize Flask extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)

# ✅ Flask-Login settings
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# ✅ Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

def generate_uid():
    """Generates a
 unique 8-character UID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_aztec_code(uid):
    """Generates an Aztec code for the given UID and saves it as an image."""
    aztec = segno.make_qr(f"https://yourwebsite.com/details/{uid}")  # Replace with actual URL
    aztec_code_path = f"static/aztec_codes/{uid}.png"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(aztec_code_path), exist_ok=True)

    # Save the Aztec code image
    aztec.save(aztec_code_path, scale=5)
    return aztec_code_path

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists! Please choose another.", "danger")
            return redirect(url_for('register'))

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create new user
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))

        flash("Invalid username or password!", "danger")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    details = Details.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", details=details)

@app.route("/add_details", methods=['GET', 'POST'])
@login_required
def add_details():
    if request.method == 'POST':
        uid = generate_uid()  

        details = Details(
            uid=uid,
            name=request.form['name'],
            emergency_contact=request.form['emergency_contact'],
            vehicle_number=request.form['vehicle_number'],
            blood_group=request.form.get('blood_group'),
            allergies=request.form.get('allergies'),
            differently_abled=request.form.get('differently_abled'),
            alternate_contact=request.form.get('alternate_contact'),
            user_id=current_user.id
        )
        db.session.add(details)
        db.session.commit()

        # Generate Aztec code
        aztec_code_path = generate_aztec_code(uid)

        # Save Aztec code path
        details.aztec_code_path = aztec_code_path
        db.session.commit()

        flash("Details added successfully! Aztec code generated.", "success")
        return redirect(url_for('dashboard'))

    return render_template("add_details.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)