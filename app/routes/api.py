import os
from app import db
from flask_login import current_user, login_required
from app.forms import PublicInfoForm
from app.models import PublicInfo, User
from flask import Blueprint, jsonify, redirect, send_from_directory, url_for

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

@api.route('/uploads/<uid>/<filename>')
@login_required
def get_image(uid, filename):
    user_folder = os.path.join('uploads', uid)
    return send_from_directory(user_folder, filename)