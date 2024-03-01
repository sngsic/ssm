from .extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    # mobile_number = db.Column(db.String(10), index=True, unique=True)
    password_hash = db.Column(db.String(128),nullable=False)
    verification_code = db.Column(db.String(6),default="111111")
    verified = db.Column(db.Boolean, default=False)
    blocked = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    public_info = db.relationship('PublicInfo', backref='user', uselist=False)

    def __repr__(self):
        return f"<User {self.username} {self.id}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PublicInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    name = db.Column(db.String(100))#, nullable=False)
    dob = db.Column(db.Date)#, nullable=False)
    gender = db.Column(db.String(10))#, nullable=False)
    marital_status = db.Column(db.String(20))#, nullable=False)
    occupation = db.Column(db.String(100))
    hobbies = db.Column(db.String(255))
    caste = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    education = db.Column(db.String(100))
    diet = db.Column(db.String(20))#, nullable=False)
    mother_tongue = db.Column(db.String(50))
    smoking_habits = db.Column(db.Boolean)#, nullable=False)
    drinking_habits = db.Column(db.Boolean)#, nullable=False)


class PrivateInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    personal_details = db.Column(db.String(255))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    citizenship = db.Column(db.String(100))
    income = db.Column(db.Integer)
    parent_info = db.Column(db.String(255))
    disabilities = db.Column(db.String(255))
