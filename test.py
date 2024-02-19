from app import db
from app.models import *
db.create_all()
adm = Admin(username='vishak',password_hash='adminpass',is_admin=True)
db.session.add(adm)