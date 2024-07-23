from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    logusername = StringField('username', validators=[DataRequired(), Length(min=3, max=15)])
    logpassword = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=128)])
    logsubmit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=128)])
    submit = SubmitField('Sign Up')
