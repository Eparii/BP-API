from flask_restful import Resource
from flask import Flask, jsonify, request
from api import utils


class UserAPI(Resource):
    def get(self):
        request_type = request.args.get('request')
        user_id = request.args.get('user_id')
        if request_type == 'swipes':
            swipes_type = request.args.get('type')
            if swipes_type is None:
                return "Bad request", 400
            return utils.create_swipes_json(user_id, swipes_type)
        elif request_type == 'groups':
            return utils.create_groups_json(user_id)
        elif request_type == 'events':
            return utils.create_events_json(user_id)
        else:
            return "Bad request", 400
