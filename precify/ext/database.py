# -*-encoding:utf-8-*-#
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

db = SQLAlchemy()
migrate = Migrate()

class Product(db.Model):
    """
    Product model class
    ...
    Attributes
    ----------
    name : str
        Product's name
    description : str
        Product's description
    """
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    prices = db.relationship("Price", backref="product")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

class Provider(db.Model):
    """
    Provider model class
    ...
    Attributes
    ----------
    name : str
        Provider's name
    description : str
        Provider's description
    """
    __tablename__ = "providers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    prices = db.relationship("Price", backref="provider")

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

class Price(db.Model):
    """
    Price model class 
    ...
    Attributes
    ----------
    product_id : int
        A product id primary key
    provider_id : int
        A provider id primary key
    price : float
        Product's price in this particular provider
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, default=None)

    db.UniqueConstraint(product_id, provider_id)
    
    def __init__(self, product_id, provider_id, price):
        self.product_id = product_id
        self.provider_id = provider_id
        self.price = price   
    
    def __str__(self):
        return str(self.price)

def init_app(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
