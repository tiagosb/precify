from flask_marshmallow import Marshmallow
from .database import Product


ma = Marshmallow()


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()


def init_app(app):
    ma.init_app(app)