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
    is_logged_in = db.Column(db.Boolean, default=False)  # Add this line

    images = db.relationship('Image', backref='user', lazy=True)
    public_info = db.relationship('PublicInfo', backref='user', uselist=False)
    # private_info = db.relationship('PrivateInfo', backref='user', uselist=False)

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



class PublicInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.String(64), db.ForeignKey('user.uid'), nullable=False)
    name = db.Column(db.String(100), nullable=False) #split
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    marital_status = db.Column(db.String(20), nullable=False)
    occupation = db.Column(db.String(100))
    hobbies = db.Column(db.String(255))
    caste = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    education = db.Column(db.String(100))
    diet = db.Column(db.String(20), nullable=False)
    mother_tongue = db.Column(db.String(50))
    smoking_habits = db.Column(db.Boolean, nullable=False)
    alcohol_intake = db.Column(db.Boolean, nullable=False)

    

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    login_time = db.Column(db.DateTime, nullable=True)
    logout_time = db.Column(db.DateTime, nullable=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), db.ForeignKey('user.uid'), nullable=False)
    filename = db.Column(db.String(150), nullable=False)
    file_path = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())