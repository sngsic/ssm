from flask import url_for, redirect, flash, render_template, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app,db
from app.models import *
from app.forms import  LoginForm, SignupForm
from functools import wraps


@app.route("/", methods=["GET", "POST"])
def home():
    signupform = SignupForm()
    loginform = LoginForm()
    
    if current_user.is_authenticated:
        print("\n\n\n\n\n\\n\n\n\n\n\n\nya")
        return redirect(url_for("profile"))  # Redirect to profile if user is already logged in

    if signupform.validate_on_submit() and "signup" in request.form:
        # Signup logic
        user = User.query.filter_by(username=signupform.username.data).first()
        if user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for("home"))
    
        verification_code = "111111" #generate_verification_code()

        # Create new user and save to database
        new_user = User(username=signupform.username.data)#, mobile_number=signupform.mobile_number.data)
        new_user.set_password(signupform.password.data)
        new_user.verification_code = verification_code  # Store verification code
        db.session.add(new_user)
        db.session.commit()

        # Send verification code via SMS
        #send_sms_verification_code(new_user.mobile_number, verification_code)

        flash("Verification code sent to your mobile number. Please verify to complete signup.", "success")
        return redirect(url_for("verify", username=new_user.username))  # Redirect to verification page
            
    elif loginform.validate_on_submit() and "login" in request.form:
            # Login logic
            user = User.query.filter_by(username=loginform.username.data).first()
            if user and user.check_password(loginform.password.data):
                login_user(user)
                return redirect(url_for("profile"))
            else:
                flash("Invalid username or password.", "danger")
    
    return render_template("index.html", registerform=signupform, loginform=loginform)

# Route for verification page
@app.route("/verify/<username>", methods=["GET", "POST"])
def verify(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("home"))
    
    if request.method == "POST":
        entered_code = request.form.get("verification_code")
        if entered_code == user.verification_code:
            user.verified = True  # Mark user as verified
            db.session.commit()
            login_user(user)
            flash("Verification successful. You are now signed up.", "success")
            return redirect(url_for("profile"))
        else:
            flash("Invalid verification code. Please try again.", "danger")
    
    return render_template("verify.html", username=username)

# Route for user profile page
@app.route("/profile")
@login_required
def profile():
    all_users = User.query.all()
    return render_template("profile.html", all_users=all_users)

# Route for user logout
@app.route("/logout",methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

