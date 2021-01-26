from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .database import db, Product, Provider, Price

admin = Admin(name="Precify", template_mode="bootstrap3")

class ProductView(ModelView):
    column_exclude_list = ['prices', ]
    form_excluded_columns = ['prices', 'created']

class ProviderView(ModelView):
    column_exclude_list = ['prices', ]
    form_excluded_columns = ['prices', 'created']

class PriceView(ModelView):
    column_list = ["product", "provider", "price", "created", "updated"]

admin.add_view(ProductView(Product, db.session))
admin.add_view(ProviderView(Provider, db.session))
admin.add_view(PriceView(Price, db.session))

def init_app(app):
    admin.init_app(app)
