from flask_babelex import Babel


babel = Babel(default_locale="pt")


def init_app(app):
    babel.init_app(app)
