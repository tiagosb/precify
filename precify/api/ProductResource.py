from flask import abort, request
from flask_restful import Resource, reqparse
from precify.ext.database import Product, db
from precify.ext.serializer import ProductSchema
from sqlalchemy.exc import IntegrityError


class ProductResource(Resource):
    """
    Product class resource
    """

    def __init__(self):
        self.schema = ProductSchema(many=True)
        self.product_parser = reqparse.RequestParser()
        self.product_parser.add_argument(
            "name", required=True, help="Product name is required"
        )
        self.product_parser.add_argument(
            "description", required=True, help="Product description is required"
        )

    def get(self):

        per_page = 2  # Refatorar para que seja uma configuração global

        parser = reqparse.RequestParser()
        parser.add_argument(
            "id",
            type=int,
            help="Product id should be a integer",
        )
        parser.add_argument(
            "page",
            type=int,
            default=1,
            help="Page number should be a integer",
        )
        args = parser.parse_args()

        if args["id"] == None:

            if args["page"] < 1:
                args["page"] = 1

            query = Product.query.paginate(args["page"], per_page, False)

            if args["page"] > 1 and args["page"] > query.pages:
                abort(404, "Page not found.")

            json_data = self.schema.dump(query.items)
            return {
                "page": args["page"],
                "products": json_data,
                "total": query.total,
                "pages": query.pages,
                "per_page": per_page,
                "next": query.has_next,
                "prev": query.has_prev,
            }, 200

        product = Product.query.get(args["id"])
        if not product:
            abort(404, "Product not found.")

        return self.schema.dump(product, many=False)

    def post(self):

        args = self.product_parser.parse_args()
        try:
            new_product = Product(args["name"], args["description"])
            db.session.add(new_product)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(
                409,
                "Ops.. conflict. Product name should be unique, identical product found.",
            )
        except Exception as error:
            db.session.rollback()
            abort(500, "Ops.. error, product can't be saved. Please, try again.")
        return self.schema.dump(new_product, many=False), 201

    def delete(self):

        parser = reqparse.RequestParser()
        parser.add_argument(
            "id", type=int, help="Product id should be a integer number"
        )
        args = parser.parse_args()

        if not args["id"]:
            abort(400, "Ops.. you should inform the product id to delete.")

        product = Product.query.get(args["id"])
        if not product:
            abort(
                404,
                "Product not found. No product with id equals {}".format(args["id"]),
            )

        try:
            db.session.delete(product)
            db.session.commit()
        except Exception as error:
            print(error)
            db.session.rollback()
            abort(
                500, "Ops.. error. Can't delete the product. Please, try again later."
            )

        return {}, 204

    def put(self):

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, required=True, help="Missing product id")
        parser.add_argument("name", required=False, help="Product name should be text")
        parser.add_argument(
            "description", required=False, help="Product should be text"
        )
        args = parser.parse_args()

        # no name or description args
        if not (args["name"] or args["description"]):
            abort(
                400, "Data is missing. You should inform new name/description to change"
            )

        product = Product.query.get(args["id"])
        if not product:
            abort(404, "Product not found.")

        if args["name"]:
            product.name = args["name"]

        if args["description"]:
            product.description = args["description"]

        try:
            db.session.commit()
            return self.schema.dump(product, many=False), 200
        except IntegrityError:
            db.session.rollback()
            abort(
                409,
                "Ops.. duplicated error, can't save the change because another product has the same name.",
            )
        except Exception as error:
            db.session.rollback()
            abort(
                500,
                "Ops.. internal server error, can't update the product. Please, try again.",
            )
