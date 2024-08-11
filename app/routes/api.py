import os
from PIL import Image
import io

from app import db
from flask_login import current_user, login_required
from app.forms import PublicInfoForm
from app.models import Image, PublicInfo, User
from flask import Blueprint, current_app, jsonify, redirect, request, send_file, send_from_directory, url_for

from werkzeug.utils import secure_filename

api = Blueprint('api', __name__,url_prefix='/api')

@api.route('/get_users')
def get_users():
    users = User.query.all()
    print('\n\n\n\n\n\n\n\n\n\n\n', users)
    user_list = [{'username': user.username, 'uid':user.uid , 'role': user.role} for user in users]
    return jsonify(user_list)

@api.route('/add_public_info', methods=['POST','GET'])
def add_public_info():
    form = PublicInfoForm()
    if form.validate_on_submit():
        public_info = PublicInfo(
            name=form.name.data,
            dob=form.dob.data,
            gender=form.gender.data,
            marital_status=form.marital_status.data,
            occupation=form.occupation.data,
            hobbies=form.hobbies.data,
            caste=form.caste.data,
            religion=form.religion.data,
            education=form.education.data,
            diet=form.diet.data,
            mother_tongue=form.mother_tongue.data,
            smoking_habits=form.smoking_habits.data,
            alcohol_intake=form.alcohol_intake.data,
            user_uid=current_user.uid  # Assuming you have current_user available via Flask-Login
        )
        db.session.add(public_info)
        db.session.commit()
    return redirect(url_for('admin.users'))


@api.route('/get_public_info', methods=['GET'])
@login_required
def get_public_info():
    # Query the public info for the current user
    public_info = PublicInfo.query.filter_by(user_id=current_user.id).first()
    
    if public_info:
        # Prepare data to be returned as JSON
        data = {
            'name': public_info.name,
            'dob': public_info.dob,
            'gender': public_info.gender,
            'marital_status': public_info.marital_status,
            'occupation': public_info.occupation,
            'hobbies': public_info.hobbies,
            'caste': public_info.caste,
            'religion': public_info.religion,
            'education': public_info.education,
            'diet': public_info.diet,
            'mother_tongue': public_info.mother_tongue,
            'smoking_habits': public_info.smoking_habits,
            'alcohol_intake': public_info.alcohol_intake
        }
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Public info not found'}), 404



@api.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if len(current_user.images) >= 5:
        return jsonify({'error': 'You can only upload up to 5 images'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.uid)
        
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        file_path = os.path.join(user_folder, filename)
        try:
            file.save(file_path)
            new_image = Image(uid=current_user.uid, filename=filename, file_path=file_path)
            db.session.add(new_image)
            db.session.commit()
            
            return jsonify({
                'success': 'Image uploaded successfully',
                'id': new_image.id,
                'url': url_for('api.get_image', uid=current_user.uid, filename=filename)
            }), 200
        except Exception as e:
            return jsonify({'error': 'Failed to upload image'}), 500
    
    return jsonify({'error': 'Failed to upload image'}), 500

@api.route('/get_images/<uid>', methods=['GET'])
@login_required
def get_images(uid):
    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], uid)
    if not os.path.exists(user_folder):
        return jsonify({'error': 'User folder does not exist'}), 404
    
    image_files = []
    for filename in os.listdir(user_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_files.append(url_for('api.get_image', uid=uid, filename=filename, _external=True))
    
    return jsonify({'images': image_files}), 200

@api.route('/get_image/<uid>/<filename>', methods=['GET'])
@login_required
def get_image(uid, filename):
    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], uid)
    return send_from_directory(user_folder, filename)




@api.route('/upload_profile_pic', methods=['POST'])
@login_required
def upload_profile_pic():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        # Define the filename to be used for the profile picture
        filename = 'profile_pic.jpg'
        user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.uid, 'profile_pic')
        
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        file_path = os.path.join(user_folder, filename)
        try:
            # Save the file with the new name
            file.save(file_path)
            return jsonify({
                'success': 'Profile picture uploaded successfully',
                'url': url_for('api.get_profile_pic', uid=current_user.uid)
            }), 200
        except Exception as e:
            return jsonify({'error': 'Failed to upload image'}), 500
    
    return jsonify({'error': 'Failed to upload image'}), 500


@api.route('/get_profile_pic/<uid>')
def get_profile_pic(uid):
    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], uid, 'profile_pic')
    filename = 'profile_pic.jpg'
    file_path = os.path.join(user_folder, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/jpeg')
    else:
        # Return a placeholder image or a message indicating no profile picture
        return send_from_directory('static', 'default_profile_pic.png')