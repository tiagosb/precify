from flask_restful import Api
from .ProductResource import ProductResource
from .ProviderResource import ProviderResource

api = Api(prefix="/api/v1")
api.add_resource(ProductResource, "/products")
api.add_resource(ProviderResource, "/providers")


def init_app(app):
    api.init_app(app)
