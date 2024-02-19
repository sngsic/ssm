# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_admin import Admin
# from .admin import MyAdminIndexView

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config.from_object('config.Config')  # Load configuration from Config class in config.py

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'
# admin = Admin(app, index_view=MyAdminIndexView())
# admin = Admin(app, name="Admin Dashboard", template_mode="bootstrap3")

from app.routes import *
# from app import routes, models
