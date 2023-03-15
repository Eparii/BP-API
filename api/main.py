from flask_restful import Resource
from flask import Flask, jsonify, request
from api import utils, dicts, db
from api.models import Swipe, Movie, MovieGenre, MovieVoD


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
        page_num = request.args.get('page')
        page_size = request.args.get('page_size')
        if page_num is None:
            page_num = 1
        else:
            page_num = int(page_num)
        if page_size is None:
            page_size = 20
        else:
            page_size = int(page_size)
        movie = utils.create_movies_json(movie_id, page_num, page_size)
        if len(movie) == 4:  # pozadavek na seznam filmu
            return movie
        else:
            return jsonify(movie=movie)

    def post(self):
        genres = []
        vods = []
        for genre_id in request.json['genres']:
            genre = MovieGenre(id_genre=genre_id)
            genres.append(genre)
        for vod_id in request.json['vods']:
            if vod_id == 'Netflix':
                vod_id = 1
            else:
                vod_id = 2
            vod = MovieVoD(id_vod=vod_id)
            vods.append(vod)
        new_movie = Movie(
            name=request.json['name'],
            release_year=request.json['release_year'],
            image_url=request.json['image_url'],
            rating=request.json['rating'],
            description=request.json['description'],
            genres=genres,
            vods=vods
        )
        db.session.add(new_movie)
        db.session.commit()
        return "", 204


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


class SwipeAPI(Resource):
    def post(self):
        new_swipe = Swipe(
            type=request.json['swipe_type'],
            id_user=int(request.json['user_id']),
            id_movie=int(request.json['movie_id']),
        )
        db.session.add(new_swipe)
        db.session.commit()
        return "", 204

    def put(self):
        user_id = int(request.json['user_id']),
        movie_id = int(request.json['movie_id']),
        swipe = Swipe.query.filter_by(id_user=user_id, id_movie=movie_id)[0]
        swipe.type = request.json['swipe_type']
        db.session.commit()
        return "", 204

    def delete(self):
        movie_id = int(request.args.get('movie_id'))
        user_id = int(request.args.get('user_id'))
        swipe = Swipe.query.filter_by(id_user=user_id, id_movie=movie_id)[0]
        db.session.delete(swipe)
        db.session.commit()
        return "", 204
