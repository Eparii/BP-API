from flask_restful import Resource
from flask import Flask, jsonify, request
from api import utils, dicts, db
from api.models import Swipe, Movie, MovieGenre, MovieVoD, Group, Genre, GroupVoD, GroupGenre, User, UserGroup
import hashlib


def get_genres_and_vods():
    vods = []
    genres = []
    for genre_name in request.json.get('genres'):
        id_genre = Genre.query.filter_by(name=genre_name).first().id
        genre = GroupGenre(id_genre=id_genre)
        genres.append(genre)
    for vod_name in request.json.get('vods'):
        vod_id = None
        if vod_name == 'Netflix':
            vod_id = 1
        else:
            vod_id = 2
        vod = GroupVoD(id_vod=vod_id)
        vods.append(vod)
    return genres, vods


class GroupManagementAPI(Resource):
    def post(self):  # pripojeni se ke skupine
        group_code = request.json.get('group_code')
        group = Group.query.filter_by(group_code=group_code).first()
        if group is None:
            return {'message': 'Invalid group code.'}, 400
        user_id = int(request.json.get('user_id'))
        user = User.query.filter_by(id=user_id).first()
        if group in user.owner_groups or group in user.member_groups:
            return {'message': 'Already member'}, 400
        new_group_member = UserGroup(id_group=group.id, id_user=user_id)
        db.session.add(new_group_member)
        db.session.commit()
        return "", 204

    def put(self):  # slouzi na zmenu majitele
        new_owner_email = request.json.get('new_owner_email')
        group_id = request.json.get('group_id')
        new_owner = User.query.filter_by(email=new_owner_email).first()
        new_member = UserGroup.query.filter_by(id_group=group_id, id_user=new_owner.id).first()
        group = Group.query.filter_by(id=group_id).first()
        old_owner_id = group.id_owner
        group.id_owner = new_owner.id
        new_member.id_user = old_owner_id
        db.session.commit()
        return "", 204

    def delete(self):  # odstraneni clenu ze skupiny ci opusteni skupiny
        group_id = request.args.get('group_id')
        user_email = request.args.get('user_email')
        user = User.query.filter_by(email=user_email).first()
        user_group = UserGroup.query.filter_by(id_user=user.id, id_group=group_id).first()
        db.session.delete(user_group)
        db.session.commit()
        return "", 204


class LoginAPI(Resource):
    def post(self):
        email = request.json.get('email')
        user = User.query.filter_by(email=email).first()
        if user is None:
            return jsonify({'message': 'Email not found'}), 404
        password = request.json.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash == password_hash:
            return {'message': 'Authentication successful', 'user_id': user.id}, 200
        else:
            return {'message': 'Incorrect password'}, 401


class RegisterAPI(Resource):
    def post(self):
        email = request.json.get('email')
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return {'message': 'Email already exists'}, 409
        password = request.json.get('password')
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(
            first_name=request.json.get('first_name'),
            last_name=request.json.get('last_name'),
            email=email,
            password_hash=password_hash
        )
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Registration successful'}, 201


class UserAPI(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        swipes = utils.create_user_swipes_json(user_id)
        groups = utils.create_user_groups_json(user_id)
        user = utils.create_user_json(user_id, swipes, groups)
        if type(user) is tuple:
            return user
        else:
            return jsonify(user=user)

    def put(self):
        user_id = int(request.json.get('user_id'))
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        email = request.json.get('email')
        password = request.json.get('password')
        user = User.query.filter_by(id=user_id).first()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password is not None:
            user.password_hash = hashlib.sha256(password.encode()).hexdigest()
        db.session.commit()
        return "", 204


class MovieAPI(Resource):
    def get(self):
        movie_id = request.args.get('movie_id')
        page_num = request.args.get('page')
        page_size = request.args.get('page_size')
        group_id = request.args.get('group_id')
        user_id = request.args.get('user_id')
        if page_num is None:
            page_num = 1
        else:
            page_num = int(page_num)
        if page_size is None:
            page_size = 100
        else:
            page_size = int(page_size)
        movie = utils.create_movies_json(movie_id, page_num, page_size, group_id, user_id)
        if len(movie) == 4:  # pozadavek na seznam filmu
            return movie
        else:
            return jsonify(movie=movie)

    def post(self):
        genres = []
        vods = []
        for genre_id in request.json.get('genres'):
            genre = MovieGenre(id_genre=genre_id)
            genres.append(genre)
        for vod_name in request.json.get('vods'):
            if vod_name == 'Netflix':
                vod_id = 1
            else:
                vod_id = 2
            vod = MovieVoD(id_vod=vod_id)
            vods.append(vod)
        new_movie = Movie(
            name=request.json.get('name'),
            release_year=request.json.get('release_year'),
            image_url=request.json.get('image_url'),
            rating=request.json.get('rating'),
            description=request.json.get('description'),
            tmdb_id=request.json.get('tmdb_id'),
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

    def post(self):
        genres, vods = get_genres_and_vods()
        new_group = Group(
            id_owner=int(request.json.get('user_id')),
            name=request.json.get('name'),
            genres=genres,
            vods=vods
        )
        db.session.add(new_group)
        db.session.commit()
        return "", 204

    def put(self):
        group_id = int(request.json.get('group_id')),
        group = Group.query.filter_by(id=group_id).first()
        old_genres = GroupGenre.query.filter_by(id_group=group_id)
        old_vods = GroupVoD.query.filter_by(id_group=group_id)
        old_genres.delete()
        old_vods.delete()
        name = request.json.get('name')
        genres, vods = get_genres_and_vods()
        group.vods = vods
        group.genres = genres
        if name is not None:
            group.name = name
        db.session.commit()
        return "", 204

    def delete(self):
        group_id = int(request.args.get('group_id'))
        group = Group.query.filter_by(id=group_id)[0]
        db.session.delete(group)
        db.session.commit()
        return "", 204


class SwipeAPI(Resource):
    def post(self):
        user_id = int(request.json.get('user_id'))
        swipe_type = request.json.get('swipe_type')
        movie_id = int(request.json.get('movie_id'))
        new_swipe = Swipe(
            type=swipe_type,
            id_user=user_id,
            id_movie=movie_id,
        )
        user = User.query.filter_by(id=user_id).first()
        group_ids = [group.id_group for group in user.owner_groups] + [group.id_group for group in user.member_groups]
        db.session.add(new_swipe)
        db.session.commit()
        matched_groups = []
        for group_id in group_ids:
            group = utils.create_group_json(group_id)
            group_members = len(group['members']) + 1  # + majitel
            if any(match['id_movie'] == movie_id and match['matched'] == group_members for match in group['matches']):
                matched_groups.append(group['name'])
        response_data = {
            "message": "success",
            "matched_groups": matched_groups
        }
        return response_data, 200

    def put(self):
        user_id = int(request.json.get('user_id')),
        movie_id = int(request.json.get('movie_id')),
        swipe = Swipe.query.filter_by(id_user=user_id, id_movie=movie_id)[0]
        swipe.type = request.json.get('swipe_type')
        db.session.commit()
        return "", 204

    def delete(self):
        movie_id = int(request.args.get('movie_id'))
        user_id = int(request.args.get('user_id'))
        swipe = Swipe.query.filter_by(id_user=user_id, id_movie=movie_id)[0]
        db.session.delete(swipe)
        db.session.commit()
        return "", 204
