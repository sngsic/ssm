from flask_login import login_required
from app.forms import CreateUserForm, LoginForm, PublicInfoForm, SignupForm
from flask import Blueprint, render_template, redirect, url_for

from app.models import User

data_entry = Blueprint('data_entry', __name__, url_prefix='/data_entry')

@login_required
@data_entry.route('/index')
def index():
    login_form = LoginForm()
    signup_form = SignupForm()
    form = PublicInfoForm()
    createuser = CreateUserForm()
    users = User.query.all()
    return render_template('data_entry/index.html', users=users, form=form, createuser=createuser, login_form=login_form, signup_form=signup_form)