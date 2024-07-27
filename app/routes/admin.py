import os
import shutil
from app.models import AdminLog, Image, PublicInfo, User
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from app.forms import CreateUserForm, PublicInfoForm, SignupForm, LoginForm
from flask_login import current_user, login_required, logout_user
from app.extensions import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/admin_auth', methods=['GET','POST'])
def admin_auth():
    signup_form = SignupForm()
    login_form = LoginForm()
    
    return render_template('admin/admin_auth.html', login_form=login_form, signup_form=signup_form)

@login_required
@admin.route('/')
@admin.route('/index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("admin.admin_auth"))
    admin_logs = AdminLog.query.all()
    return render_template('admin/admin_index.html', logs=admin_logs)

@admin.route('/users')
def users():
    form = PublicInfoForm()
    createuser = CreateUserForm()
    if not current_user.is_authenticated:
        return redirect(url_for("admin.admin_auth"))
    users = User.query.all()
    return render_template('admin/user_list.html', users = users, form=form, createuser=createuser)

@admin.route('/public_info')
@login_required
def public_info():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.admin_login"))
    public_infos = PublicInfo.query.all()
    return render_template('admin/public_info.html', public_infos=public_infos)

@admin.route('/delete_user/<uid>')
def delete_user(uid):
    if not current_user.is_authenticated:
        return redirect(url_for("admin.admin_auth"))
    
    user = User.query.get(uid)
    if user:
        # Delete associated images
        images = Image.query.filter_by(uid=uid).all()
        for image in images:
            # Delete image from filesystem
            if os.path.exists(image.file_path):
                os.remove(image.file_path)
            # Delete image record from database
            db.session.delete(image)
        
        # Delete user folder from filesystem
        user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], uid)
        if os.path.exists(user_folder):
            shutil.rmtree(user_folder) 

        # Delete user record from database
        db.session.delete(user)
        db.session.commit()
        
        return redirect(url_for('admin.users'))
    
    return redirect(url_for('admin.users'))

@admin.route('/edit_user/<uid>',methods=['POST'])
def edit_user(uid):
    if not current_user.is_authenticated:
        return redirect(url_for("admin.admin_auth"))
    user = User.query.get(uid)
    if user:
        user.username = request.form.get('username')
        user.role = request.form.get('role')
        db.session.commit()
        flash('User updated successfully', 'success')
    else:
        flash('User not found', 'danger')
    
    return redirect(url_for('admin.users'))

@admin.route('/clear_logs')
# @login_required
def clear_logs():
    users = User.query.all()
    logout_user()
    for user in users:
        user.is_logged_in = False
    AdminLog.query.delete()
    db.session.commit()
    
    return redirect(url_for('admin.index'))


@admin.route('/add_user', methods=['GET','POST'])
def add_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            return redirect(url_for('admin.index'))

        # Create a new user
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        # Optionally, set other attributes like role, generate uid, etc.
        new_user.generate_uid()

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        # Create user folder for storing files
        user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], new_user.uid)
        os.makedirs(user_folder, exist_ok=True)


        return redirect(url_for('admin.users'))  # Redirect to admin index after successful user creation

    return render_template('admin.html', form=form)

@admin.route('/delete_public')
def delete_public():
    PublicInfo().query.delete()
    db.session.commit()
    return redirect(url_for('admin.public_info'))