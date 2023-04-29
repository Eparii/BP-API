from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from api.variables import db, bcrypt

from api.main import UserAPI, MovieAPI, GroupAPI, SwipeAPI, LoginAPI, RegisterAPI, GroupManagementAPI


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
    my_api.add_resource(MovieAPI, '/movie')
    my_api.add_resource(GroupAPI, '/group')
    my_api.add_resource(SwipeAPI, '/swipe')
    my_api.add_resource(LoginAPI, '/login')
    my_api.add_resource(RegisterAPI, '/register')
    my_api.add_resource(GroupManagementAPI, '/groupManagement')

    return app
