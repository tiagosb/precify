# -*-encoding:utf-8-*-#
from flask import Flask
from .ext import database, serializer, admin, language
from .api import api
from .blueprints import views

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///precify.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "secretkey"
    
    views.init_app(app)
    database.init_app(app)
    serializer.init_app(app)
    api.init_app(app)
    admin.init_app(app)
    language.init_app(app)
    return app
