import os
from flask import Blueprint, current_app, flash, redirect, render_template, send_from_directory, url_for
from flask_login import current_user, login_required
from app.forms import ImageUploadForm, PublicInfoForm
from app.models import Image
from app import db

main = Blueprint('main',__name__)

@login_required
@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html')

# @login_required
@main.route('/profile')
def profile():
    form = PublicInfoForm()
    if current_user.is_authenticated:
        return render_template('main/profile.html', form=form)
    return redirect(url_for('main.index'))



@main.route('/images', methods=['GET'])
@login_required
def images():
    form = ImageUploadForm()
    
    images = Image.query.filter_by(uid=current_user.uid).all()
    return render_template('main/images.html', form=form, images=images)