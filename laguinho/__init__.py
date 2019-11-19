from flask import Flask
from .extensions import mongo


def register_blueprints(app):
    from .errors.handlers import errors
    from .routes.datasets import datasets
    from .routes.microservices import microservices
    app.register_blueprint(errors)
    app.register_blueprint(datasets)
    app.register_blueprint(microservices)


def create_app(config='laguinho.config.BaseConfig'):
    app = Flask(__name__)
    app.config.from_object(config)

    mongo.init_app(app)

    register_blueprints(app)

    @app.route('/')
    def hello_world():
        return 'Laguinho API is up and running.'

    return app
