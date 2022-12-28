from flask_restful import Resource
from flask import Flask, jsonify, request
from api import utils


class UserAPI(Resource):
    def get(self):
        request_type = request.args.get('request')
        user_id = request.args.get('user_id')
        if request_type == 'swipes':
            swipes_type = request.args.get('type')
            return utils.create_user_swipes_json(user_id, swipes_type)
        elif request_type == 'groups':
            return utils.create_user_groups_json(user_id)
        elif request_type == 'events':
            return utils.create_user_events_json(user_id)
        else:
            return "Bad request", 400


class MovieAPI(Resource):
    def get(self):
        movie_id = request.args.get('movie_id')
        return utils.create_movies_json(movie_id)


class GroupAPI(Resource):
    def get(self):
        group_id = request.args.get('group_id')
        return utils.create_group_json(group_id)


class EventAPI(Resource):
    def get(self):
        event_id = request.args.get('event_id')
        return utils.create_event_json(event_id)

