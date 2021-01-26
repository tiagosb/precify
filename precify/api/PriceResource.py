from flask_restful import Resource, reqparse
from precify.ext.database import db, Price
from precify.ext.serializer import PriceSchema
from flask import abort
from sqlalchemy.exc import IntegrityError


class PriceResource(Resource):
    """
    Price model class
    """
    def __init__(self):
        self.schema = PriceSchema()
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("product_id", type=int, help="Product id should be a integer number.", required=True)
        parser.add_argument("provider_id", type=int, help="Provider id should be a integer number.", required=True)
        parser.add_argument("price", type=float, help="Price should be a float number.", required=True)
        
        args = parser.parse_args()
        try:
            new_price = Price(args["product_id"], args["provider_id"], args["price"])
            db.session.add(new_price)
            db.session.commit()
            return self.schema.dump(new_price, many=False), 201
        except IntegrityError:
            db.session.rollback()
            abort(409, "Ops.. integrity error.")
        except Exception as error:
            db.session.rollback()
            abort(500, "Error, can't save data. Please try again.")
