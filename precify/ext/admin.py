from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .database import db, Product

admin = Admin(name="Precify", template_mode="bootstrap3")

admin.add_view(ModelView(Product, db.session))

def init_app(app):
    admin.init_app(app)