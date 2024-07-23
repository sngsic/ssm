from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer)
    username = db.Column(db.String(64), index=True, unique=True)
    uid = db.Column(db.String(64), unique=True, nullable=False, primary_key=True)
    password_hash = db.Column(db.String(128),nullable=False)
    role = db.Column(db.String(64), default='admin')
    status = db.Column(db.Boolean, default=False)
    note = db.Column(db.String(1024), default='None', nullable=True)
    
    def generate_uid(self):
        # Generate uid based on username, month, and year
        username_part = self.username[:3].lower()  # First 3 characters of username, converted to lowercase
        month_part = datetime.now().strftime("%m")  # Current month as two digits (e.g., '06')
        year_part = datetime.now().strftime("%Y")[-2:]  # Last two digits of the current year (e.g., '24')
        self.uid = f"{username_part}{month_part}{year_part}"
        
    def __repr__(self):
        return f"<User {self.username} {self.uid}>"
    
    def toggle_block(self):
        self.status = not self.status

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.uid
    

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    login_time = db.Column(db.DateTime, nullable=True)
    logout_time = db.Column(db.DateTime, nullable=True)