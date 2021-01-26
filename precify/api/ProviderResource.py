# -*- coding: utf-8 -*-
from flask import abort
from flask_restful import Resource, reqparse
from precify.ext.database import Provider, db
from precify.ext.serializer import ProductSchema
from sqlalchemy.exc import IntegrityError


class ProviderResource(Resource):
    def __init__(self):
        self.schema = ProductSchema()

    def get(self):
        per_page = 2  # Refatorar para que seja uma configuração global
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, help="Id should be a integer.")
        parser.add_argument(
            "page", type=int, default=1, help="Page shoud be a integer."
        )
        args = parser.parse_args()

        if args["id"] == None:
            if args["page"] < 1:
                args["page"] = 1

            query = Provider.query.paginate(args["page"], per_page, False)

            if args["page"] > 1 and args["page"] > query.pages:
                abort(404, "Page not found.")

            json_data = self.schema.dump(query.items, many=True)
            return {
                "page": args["page"],
                "providers": json_data,
                "total": query.total,
                "pages": query.pages,
                "per_page": per_page,
                "next": query.has_next,
                "prev": query.has_prev,
            }, 200

        provider = Provider.query.get(args["id"])
        if not provider:
            abort(404, "Provider not found.")
        return self.schema.dump(provider), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("description", required=True)

        args = parser.parse_args()
        new_provider = Provider(args["name"], args["description"])
        db.session.add(new_provider)
        try:
            db.session.commit()
            return {
                "id": new_provider.id,
                "name": new_provider.name,
                "description": new_provider.description,
            }, 201
        except IntegrityError:
            abort(
                409,
                "Ops.. conflict. Provider name should be unique, identical provider found.",
            )
        except Exception as error:
            abort(
                500, "Ops.. error, can't save provider data. Please, try again later."
            )
