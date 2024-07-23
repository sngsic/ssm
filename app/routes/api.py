from app.models import User
from flask import Blueprint, jsonify

api = Blueprint('api', __name__,url_prefix='/api')

@api.route('/get_users')
def get_users():
    users = User.query.all()
    print('\n\n\n\n\n\n\n\n\n\n\n', users)
    user_list = [{'username': user.username, 'uid':user.uid , 'role': user.role} for user in users]
    return jsonify(user_list)