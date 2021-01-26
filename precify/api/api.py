from flask_restful import Api
from .ProductResource import ProductResource
from .ProviderResource import ProviderResource
from .PriceResource import PriceResource 

api = Api(prefix="/api/v1")
api.add_resource(ProductResource, "/products")
api.add_resource(ProviderResource, "/providers")
api.add_resource(PriceResource, "/prices")

def init_app(app):
    api.init_app(app)
