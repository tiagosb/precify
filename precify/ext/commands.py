import click
from precify.ext.database import db, Price, Provider, Product

def init_app(app):
    @app.cli.command()
    def create_db():
        click.echo("Creating db..")
        db.create_all()

    @app.cli.command()
    def delete_db():
        click.echo("Deleting db..")
        db.drop_all()
