from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

main = Blueprint('main',__name__)

@login_required
@main.route('/')
@main.route('/index')
def index():
    return render_template('main/index.html')

@login_required
@main.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('main/profile.html')
    return redirect(url_for('main.index'))