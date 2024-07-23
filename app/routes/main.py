from flask import Blueprint

main = Blueprint('main',__name__)


@main.route('/index')
def index():
    return 'hello'
