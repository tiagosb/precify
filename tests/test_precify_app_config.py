from flask import Flask


def test_app_should_be_instance_of_flask(app):
    assert isinstance(app, Flask)


def test_app_env_shoud_be_testing(app):
    assert app.config["ENV"] == "testing"


def test_sqlalchemy_database_uri_should_be_memory(app):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
