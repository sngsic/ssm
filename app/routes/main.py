import os
from flask import Blueprint, current_app, flash, redirect, render_template, send_from_directory, url_for
from flask_login import current_user, login_required
from app.forms import ImageUploadForm, LoginForm, PrivateInfoForm, PublicInfoForm, SignupForm
from app.models import Image, User
from app import db

main = Blueprint('main',__name__)

@login_required
@main.route('/')
@main.route('/index')
def index():
    signup = SignupForm()
    login = LoginForm()
    return render_template('main/index.html', login_form = login, signup_form=signup)

# @login_required
@main.route('/profile', methods=['POST','GET'])
def profile():
    public_info_form = PublicInfoForm()
    private_info_form = PrivateInfoForm()
    if current_user.is_authenticated:
        return render_template('main/profile.html', public_info_form=public_info_form, private_info_form=private_info_form)
    return redirect(url_for('main.index'))


@main.route('/images', methods=['GET'])
@login_required
def images():
    form = ImageUploadForm()
    
    images = Image.query.filter_by(uid=current_user.uid).all()
    return render_template('main/images.html', form=form, images=images)

@main.route('/search')
def search():
    users = User.query.all()
    
    return render_template('main/search.html', users=users)


@main.route('/view/<uid>')
def view_profile(uid):
    user = User.query.filter_by(uid=uid).first_or_404()
    public_info = user.public_info  # Assuming `public_info` is a relationship in the User model
    return render_template('main/view_profile.html', user=user, public_info=public_info)
