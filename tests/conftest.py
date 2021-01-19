import pytest
from precify.app import create_app
from precify.ext.database import db, Product


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    yield app


@pytest.fixture(scope="session")
def client(app):
    with app.app_context():
        db.create_all()
        client = app.test_client()
        yield client
