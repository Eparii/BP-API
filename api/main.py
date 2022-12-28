from flask_restful import Resource
from flask import Flask, jsonify, request
from api import utils, dicts


class UserAPI(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        swipes = utils.create_user_swipes_json(user_id)
        groups = utils.create_user_groups_json(user_id)
        events = utils.create_user_events_json(user_id)
        user = utils.create_user_json(user_id, swipes, groups, events)
        if type(user) is tuple:
            return user
        else:
            return jsonify(user=user)


class MovieAPI(Resource):
    def get(self):
        movie_id = request.args.get('movie_id')
        movie = utils.create_movies_json(movie_id)
        if type(movie) is tuple:
            return movie
        else:
            return jsonify(movie=movie)


class GroupAPI(Resource):
    def get(self):
        group_id = request.args.get('group_id')
        group = utils.create_group_json(group_id)
        if type(group) is tuple:
            return group
        else:
            return jsonify(group=group)


class EventAPI(Resource):
    def get(self):
        event_id = request.args.get('event_id')
        event = utils.create_event_json(event_id)
        if type(event) is tuple:
            return event
        else:
            return jsonify(event=event)
