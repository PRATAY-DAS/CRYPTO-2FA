from flask import render_template, redirect, url_for, request, flash
from app import app, db, login_manager
from models import User
from flask_login import login_user, login_required, logout_user
import pyotp
import qrcode

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            otp = request.form.get("otp")
            totp = pyotp.TOTP(user.otp_secret)
            if totp.verify(otp):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid OTP.")
        else:
            flash("Invalid credentials.")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/setup")
@login_required
def setup():
    user = User.query.filter_by(username="your_username").first()  # Replace with session-based user
    totp = pyotp.TOTP(user.otp_secret)
    qr_uri = totp.provisioning_uri(name=user.username, issuer_name="Crypto2FA")
    qr = qrcode.make(qr_uri)
    qr.save("static/qrcode.png")
    return render_template("setup.html", qr_uri=qr_uri)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
