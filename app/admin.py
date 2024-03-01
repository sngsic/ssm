from .extensions import db
from flask_login import current_user
from .models import User, PublicInfo
from flask_admin import Admin, expose
from .extensions import login_manager
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm


# from flask_admin.model.form import InlineFormAdmin
# from flask_admin.model.widgets import AjaxSelect2Field
from wtforms import SelectField
from flask_admin.actions import action


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserView(ModelView):
    column_list = [
        "username",
        "id",
    ]
    column_exclude_list = ('password_hash',)
    # form_excluded_columns = ("password_hash",)
    def is_accessible(self):
        return current_user.is_authenticated #and getattr(current_user, 'is_admin',False)

    def on_model_change(self, form, model, is_created):
        # Hash the password if a new user is being created or the password field is modified
        if is_created or "password" in form.password_hash.data:
            model.set_password(form.password_hash.data)

        # If a new user is created, add corresponding entry in PublicInfo
        if is_created:
            public_info = PublicInfo(user_id=model.id)
            db.session.add(public_info)
            db.session.commit()

    @action(
        "toggle_block",
        "Toggle Block",
        "Are you sure you want to toggle selected users?",
    )
    def action_toggle_block(self, ids):
        users = User.query.filter(User.id.in_(ids)).all()
        for user in users:
            user.blocked = not user.blocked
        db.session.commit()
        flash("User block status updated successfully.", "success")
        return redirect(
            url_for("admin.index")
        )  # Redirect back to admin panel after action

    column_filters = ["blocked"]


class PublicInfoView(ModelView):
    # Customize the view as needed
    column_list = [
        "name",
        "user_id",
    ]  # Define which columns to display
    column_filters = ["name", "gender"]  # Add filters for columns
    column_searchable_list = ["name"]  # Enable searching by name

    def is_accessible(self):
        return current_user.is_authenticated and getattr(
            current_user, "is_admin", False
        )

    # def on_model_change(self, form, model, is_created):
    #     if is_created:
    #         # Associate the newly created PublicInfo row with the selected user
    #         user_id = form.user_id.data
    #         model.user = User.query.get(user_id)


admin = Admin(name="Admin Panel")
admin.add_view(UserView(User, db.session))
admin.add_view(PublicInfoView(PublicInfo, db.session))
