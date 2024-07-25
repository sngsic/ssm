from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    logusername = StringField('username', validators=[DataRequired(), Length(min=3, max=15)])
    logpassword = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=128)])
    logsubmit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=128)])
    submit = SubmitField('Sign Up')


class PublicInfoForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    marital_status = SelectField('Marital Status', choices=[('single', 'Single'), ('married', 'Married')], validators=[DataRequired()])
    occupation = StringField('Occupation')
    hobbies = StringField('Hobbies')
    caste = StringField('Caste')
    religion = StringField('Religion')
    education = StringField('Education')
    diet = SelectField('Diet', choices=[('vegetarian', 'Vegetarian'), ('non-vegetarian', 'Non-Vegetarian'), ('vegan', 'Vegan')], validators=[DataRequired()])
    mother_tongue = StringField('Mother Tongue')
    smoking_habits = BooleanField('Smoking Habits')
    alcohol_intake = BooleanField('Drinking Habits')
    