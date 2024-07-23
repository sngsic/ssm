from datetime import datetime
from flask import Blueprint, flash, render_template, url_for
from flask import request, redirect
from flask_login import current_user, login_user, logout_user

from app.forms import LoginForm, SignupForm
from app.models import AdminLog, User
from app.extensions import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/admin_login', methods = ['GET','POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        logusername = form.logusername.data
        logpassword = form.logpassword.data

        user = User.query.filter_by(username=logusername).first()
        if user and user.check_password(logpassword):
            login_user(user)
            log_entry = AdminLog(uid=user.uid, username=user.username, role='admin', login_time=datetime.now())
            db.session.add(log_entry)

            db.session.commit()
            return redirect(url_for('admin.index'))
        
        flash('Invalid username or password', 'danger')

    return render_template('admin/admin_auth.html', login_form=form, signup_form=SignupForm())


@auth.route('/admin_signup', methods=['GET','POST'])
def admin_signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.admin_login'))

        new_user = User(username=username)
        new_user.set_password(password)
        new_user.generate_uid()

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        log_entry = AdminLog(uid=new_user.uid, username=new_user.username, role='admin', login_time=datetime.now())
        db.session.add(log_entry)
        db.session.commit()

        return redirect(url_for('admin.index'))

    return render_template('admin/admin_auth.html', login_form=LoginForm(), signup_form=form)


@auth.route('/admin_logout')
def admin_logout():
    if current_user.is_authenticated:
        log_entry = AdminLog.query.filter_by(uid=current_user.uid).order_by(AdminLog.id.desc()).first()
        if log_entry and log_entry.logout_time is None:
            log_entry.logout_time = datetime.now()  # Record current time
            db.session.commit()
        logout_user()

    return redirect(url_for('admin.admin_auth'))