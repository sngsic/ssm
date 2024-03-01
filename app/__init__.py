from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .admin import admin
from .extensions import db,login_manager
from sqlalchemy import event
from app.models import User, PublicInfo
from sqlalchemy.orm import Session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config.from_object('config.Config')  # Load configuration from Config class in config.py

db.init_app(app)
admin.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'home'

def create_public_info_for_new_user(mapper, connection, target):
    # Check if the target is an instance of the User model
    if isinstance(target, User):
        # Create a new row in the PublicInfo table with the same id as the new user
        session = Session(bind=connection)
        public_info = PublicInfo(user_id=target.id)
        session.add(public_info)
        session.commit()

# Listen for the after_insert event of the User model
event.listen(User, 'before_insert', create_public_info_for_new_user)

from app.routes import *
# from app import routes, models
