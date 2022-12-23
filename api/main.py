from flask_restful import Resource
from api.models import User
from api import utils
from flask import Flask, jsonify, request


class UserAPI(Resource):
    def get(self):
        users = User.query.all()
        users_list = []
        for user in users:
            user_dict = utils.create_user_dict(user)
            users_list.append(user_dict)
        return jsonify(users=users_list)
