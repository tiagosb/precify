from flask_restful import Api
from .ProductResource import ProductResource

api = Api(prefix="/api/v1")
api.add_resource(ProductResource, "/products")


def init_app(app):
    api.init_app(app)
