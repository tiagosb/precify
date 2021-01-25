# -*-encoding:utf-8-*-#
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class Product(db.Model):
    """
    A product class model
    """
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description


def init_app(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
