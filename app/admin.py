from .models import User
from .extensions import db
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from .extensions import login_manager
from flask_login import current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated# and getattr(current_user, 'is_admin',True)

admin = Admin(name="Admin Panel")
admin.add_view(UserView(User, db.session))
