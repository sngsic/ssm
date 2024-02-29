from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .admin import admin
from .extensions import db,login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config.from_object('config.Config')  # Load configuration from Config class in config.py

db.init_app(app)
admin.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'home'

from app.routes import *
# from app import routes, models
