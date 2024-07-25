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



@main.route('/images', methods=['GET', 'POST'])
@login_required
def images():
    form = ImageUploadForm()
    
    if form.validate_on_submit():
        file = form.image.data
        if file:
            if len(current_user.images) >= 5:
                flash('You can only upload up to 5 images.', 'warning')
                return redirect(url_for('main.images'))
                
            filename = file.filename
            user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.uid)
            
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            
            file_path = os.path.join(user_folder, filename)
            try:
                file.save(file_path)
                # Save image details to database
                new_image = Image(uid=current_user.uid, filename=filename, file_path=file_path)
                db.session.add(new_image)
                db.session.commit()
                flash('Image uploaded successfully!', 'success')
            except Exception as e:
                flash('Failed to upload image.', 'danger')
            
            return redirect(url_for('main.images'))
    
    images = Image.query.filter_by(uid=current_user.uid).all()
    return render_template('main/images.html', form=form, images=images)
