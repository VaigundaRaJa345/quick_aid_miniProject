import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from quick_aid.extensions import db, bcrypt, login_manager
from quick_aid.models import User, Details
from quick_aid.config import Config
import random
import string
import segno  # Aztec Code generation

# ✅ Correct Flask instance
app = Flask(__name__)  
app.config.from_object(Config)

# ✅ Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)

# ✅ Fix login route reference
login_manager.login_view = 'auth.login'  # If login is in auth.py blueprint
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_uid():
    """Generates a unique 8-character UID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_aztec_code(uid):
    """Generates an Aztec code for the given UID."""
    url = f"https://quick-aid-miniproject-1.onrender.com/details/{uid}"  # Adjust URL as needed
    aztec = segno.make(url)

    aztec_dir = "static/aztec_codes"
    os.makedirs(aztec_dir, exist_ok=True)

    aztec_code_path = os.path.join(aztec_dir, f"{uid}.png")
    aztec.save(aztec_code_path, scale=5)

    return aztec_code_path

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aztec_code/<uid>")
def get_aztec_code(uid):
    """Serves the Aztec code image for a given UID."""
    aztec_code_path = f"static/aztec_codes/{uid}.png"
    if os.path.exists(aztec_code_path):
        return send_from_directory("static/aztec_codes", f"{uid}.png")
    else:
        flash("Aztec code not found!", "danger")
        return redirect(url_for('home'))  # ✅ Ensure this route exists

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for('auth.login'))  # ✅ Ensure this matches your actual login route

with app.app_context():
    db.create_all()

# ✅ Fix port issue for Render
if _name_ == "_main_":  # ✅ Corrected "main_"
    port = int(os.environ.get("PORT", 5000))  # Use Render's port or default to 5000
    app.run(host="0.0.0.0", port=port)
