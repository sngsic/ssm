from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from app.models import User

class SignupForm(FlaskForm):
    username = StringField('Username',id='signup-username', validators=[DataRequired(), Length(min=4, max=20)])
    # mobile_number = StringField('Mobile Number', validators=[DataRequired(), Regexp(r'^\d{10}$', message="Invalid mobile number format.")])
    password = PasswordField("Password", id="signup-pass", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",id="signup-pass-confirm",validators=[DataRequired(), EqualTo("password")],)
    submit = SubmitField('Sign Up',name='signup')


class LoginForm(FlaskForm):
    username = StringField("Username", id="login-username", validators=[DataRequired()])
    # mobile_number = StringField('Mobile Number', validators=[DataRequired(), Regexp(r'^\d{10}$', message="Invalid mobile number format.")])
    password = PasswordField("Password", id="login-pass", validators=[DataRequired()])
    submit = SubmitField("Login",name='login')

class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")