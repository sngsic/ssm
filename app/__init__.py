from .models import User
from .config import Config
from .extensions import app, db, socketio

from flask_login import LoginManager
from flask_migrate import Migrate

from .routes.admin import admin
from .routes.main import main
from .routes.auth import auth
from .routes.api import api

app.register_blueprint(admin)
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config)
migrate = Migrate()
db.init_app(app)
socketio.init_app(app, cors_allowed_origins="*")
migrate.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'index'


@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)


@app.route('/list_routes')
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, str(rule)))
        output.append(line)
    return "<pre>" + "\n".join(sorted(output)) + "</pre>"


if __name__ == '__main__':
    socketio.run(app)