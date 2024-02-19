from flask import url_for, redirect, flash, render_template, request
from flask_login import login_user, logout_user, login_required, current_user
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
from app import app,db
from app.models import *
from app.forms import  LoginForm, SignupForm, AdminLoginForm
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
    # Profile page
    return render_template("profile.html")

# Route for user logout
@app.route("/logout",methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


####################### admin
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("You are not authorized to access this page.", "danger")
            return redirect(url_for("home"))  # Redirect unauthorized users
        return func(*args, **kwargs)

    return decorated_view


# Admin login route
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid admin username or password.", "danger")
    return render_template("admin_login.html", form=form)


@app.route("/admin/dashboard")
@login_required
# @admin_required
def admin_dashboard():
    # Only accessible to authenticated admin users
    users = User.query.all()  # Get all users from the database
    return render_template("admin_dash.html", users=users)


# # Route to block/unblock user
# @app.route("/admin/block_user/<int:user_id>")
# @login_required
# # @admin_required
# def block_user(user_id):
#     user = User.query.get(user_id)
#     if user:
#         user.blocked = not user.blocked  # Toggle blocked status
#         db.session.commit()
#         flash(
#             "User has been blocked." if user.blocked else "User has been unblocked.",
#             "success",
#         )
#     else:
#         flash("User not found.", "danger")
#     return redirect(url_for("admin_dashboard"))


# # Route to display user information
# @app.route("/admin/user_info/<int:user_id>")
# @login_required
# # @admin_required
# def user_info(user_id):
#     user = User.query.get(user_id)
#     if user:
#         return render_template("user_info.html", user=user)
#     else:
#         flash("User not found.", "danger")
#         return redirect(url_for("admin_dashboard"))


# # add user
# @app.route("/admin/add_user", methods=["POST"])
# @login_required
# # @admin_required
# def add_user():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         # Perform validation as needed
#         user = User(username=username)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
#         flash("User added successfully.", "success")
#     return redirect(url_for("admin_dashboard"))


# # Route to remove a user
# @app.route("/admin/remove_user/<int:user_id>", methods=["POST"])
# @login_required
# # @admin_required
# def remove_user(user_id):
#     user = User.query.get(user_id)
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         flash("User removed successfully.", "success")
#     else:
#         flash("User not found.", "danger")
#     return redirect(url_for("admin_dashboard"))
