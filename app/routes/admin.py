from app.models import AdminLog, User
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
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

@admin.route('/delete_user/<uid>')
def delete_user(uid):
    if not current_user.is_authenticated:
        return redirect(url_for("admin.admin_auth"))
    user = User.query.get(uid)
    if user:
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