import os
from PIL import Image
import io

from app import db
from flask_login import current_user, login_required
from app.forms import PrivateInfoForm, PublicInfoForm
from app.models import Image, PrivateInfo, PublicInfo, User
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
    if current_user.role == 'admin':
        return redirect(url_for('admin.users'))
    elif current_user.role == 'user':
        return redirect(url_for('main.profile'))

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
        # Secure the filename and retain its extension
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1].lower()
        
        # Ensure the extension is one of the allowed image formats
        if extension not in ['.jpg', '.jpeg', '.png', '.gif']:
            return jsonify({'error': 'Unsupported image format'}), 400
        
        user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.uid)
        
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        file_path = os.path.join(user_folder, filename)
        try:
            # Save the file with the original extension
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
            return jsonify({'error': 'Failed to upload image', 'message': str(e)}), 500
    
    return jsonify({'error': 'Failed to upload image'}), 500

@api.route('/get_images/<uid>', methods=['GET'])
@login_required
def get_images(uid):
    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], uid)
    
    if not os.path.exists(user_folder):
        return jsonify({'error': 'User folder does not exist'}), 404
    
    image_files = []
    try:
        for filename in os.listdir(user_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_files.append(url_for('api.get_image', uid=uid, filename=filename, _external=True))
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve images', 'message': str(e)}), 500
    
    return jsonify({'images': image_files}), 200


@api.route('/get_image/<uid>/<filename>', methods=['GET'])
@login_required
def get_image(uid, filename):
    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], uid)
    file_path = os.path.join(user_folder, filename)
    
    if os.path.exists(file_path):
        # Determine MIME type based on file extension
        mime_type = None
        
        if filename.lower().endswith('.png'):
            mime_type = 'image/png'
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            mime_type = 'image/jpeg'
        elif filename.endswith('.gif'):
            mime_type = 'image/gif'
        
        if mime_type:
            return send_file(file_path, mimetype=mime_type)
    
    return jsonify({'error': 'Image not found'}), 404


@api.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    if 'image' not in request.files:
        return jsonify(success=False, error="No image part"), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify(success=False, error="No selected file"), 400

    # Check if the file has an allowed extension
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        # Set the filename to profilepic with the correct extension
        new_filename = f"profilepic.{file_ext}"

        # Define the path to the user's folder
        user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.uid, 'profilepic')

        # Create the folder if it doesn't exist
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Save the file, replacing the old profile picture
        file_path = os.path.join(user_folder, new_filename)
        file.save(file_path)

        return jsonify(success=True), 200

    return jsonify(success=False, error="File type not allowed"), 400


@api.route('/get_profile_pic/<uid>')
def get_profile_pic(uid):
    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], uid, 'profilepic')
    
    # Look for profilepic with any of the allowed extensions
    for ext in ['jpg', 'jpeg', 'png', 'gif']:
        file_path = os.path.join(user_folder, f"profilepic.{ext}")
        if os.path.exists(file_path):
            return send_from_directory(user_folder, f"profilepic.{ext}")
    
    # If no profile picture is found, return a default image or 404
    return send_from_directory('uploads', 'default_profile.png')


@api.route('/delete_profile_pic', methods=['POST'])
@login_required
def delete_profile_pic():
    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.uid, 'profilepic')
    filename = 'profilepic'  # Fixed filename for the profile picture

    # Check for file extensions
    file_extensions = ['jpg', 'jpeg', 'png', 'gif']
    file_deleted = False

    for ext in file_extensions:
        file_path = os.path.join(user_folder, f"{filename}.{ext}")
        if os.path.exists(file_path):
            os.remove(file_path)
            file_deleted = True
            break  # Exit loop once the file is deleted

    if file_deleted:
        return jsonify(success=True), 200
    else:
        return jsonify(success=False, error="Profile picture not found"), 404