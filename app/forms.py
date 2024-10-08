from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, FloatField, IntegerField, SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileField


class LoginForm(FlaskForm):
    logusername = StringField('username', validators=[DataRequired(), Length(min=3, max=15)])
    logpassword = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=128)])
    logsubmit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=128)])
    submit = SubmitField('Sign Up')


class PublicInfoForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
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
    bio = StringField("Bio")

class PrivateInfoForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    personal_details = StringField('Personal Details')
    height = FloatField('Height')
    weight = FloatField('Weight')
    citizenship = StringField('Citizenship')
    income = IntegerField('Income')
    parent_info = StringField('Parent Information')
    disabilities = StringField('Disabilities')

# preview form
class PreviewForm(FlaskForm):
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
    


class ImageUploadForm(FlaskForm):
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Upload')
    
class CreateUserForm(FlaskForm):
    username = StringField("Username", id="login-username", validators=[DataRequired()])
    # mobile_number = StringField('Mobile Number', validators=[DataRequired(), Regexp(r'^\d{10}$', message="Invalid mobile number format.")])
    password = PasswordField("Password:", id="login-pass", validators=[DataRequired()])
    submit = SubmitField("Submit",name='submit')
