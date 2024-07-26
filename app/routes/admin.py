import os
from app.models import AdminLog, Image, PublicInfo, User
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from app.forms import SignupForm, LoginForm
from flask_login import current_user, login_required
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
    if not current_user.is_authenticated:
        return redirect(url_for("admin.admin_auth"))
    users = User.query.all()
    return render_template('admin/user_list.html', users = users)

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
            os.rmdir(user_folder)  # Use os.rmdir to remove empty directory

        # Delete user record from database
        db.session.delete(user)
        db.session.commit()
        
        return redirect(url_for('admin.users'))
    
    return redirect(url_for('admin.users'))

@admin.route('/edit_user/<uid>')
def edit_user(uid):
    if not current_user.is_authenticated:
        return redirect(url_for("admin.admin_auth"))
    user = User.query.get(uid)
    if user:
        user.username = request.form['username']
        user.role = request.form['role']
        db.session.commit()
        flash('User updated successfully', 'success')
    else:
        flash('User not found', 'danger')
    
    return redirect(url_for('admin.users'))

@admin.route('/clear_logs')
@login_required
def clear_logs():
    AdminLog.query.delete()
    db.session.commit()
    
    return redirect(url_for('admin.index'))

