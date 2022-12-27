from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from api.variables import db, bcrypt

from api.main import UserAPI


def create_app(config_class=None):
    app = Flask(__name__)
    my_api = Api(app)
    CORS(app)

    if config_class is None:
        from api.config import Config
        config_class = Config

    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)

    my_api.add_resource(UserAPI, '/user')

    return app