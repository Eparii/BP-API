from api import dicts
from api.models import Swipe, Group, UserGroup, UserEvent, Event, Movie, User
from flask import jsonify


def create_user_swipes_json(user_id):
    if user_id is None:
        return "Bad request", 400
    likes = []
    dislikes = []
    likes_query = Swipe.query.filter_by(id_user=user_id, type='like')
    dislikes_query = Swipe.query.filter_by(id_user=user_id, type='dislike')
    for like in likes_query:
        likes.append(dicts.create_swipe_dict(like))
    for dislike in dislikes_query:
        dislikes.append(dicts.create_swipe_dict(dislike))
    swipes_dict = {
        "likes": likes,
        "dislikes": dislikes
    }
    return swipes_dict


def create_user_groups_json(user_id):
    if user_id is None:
        return "Bad request", 400
    owner_groups = Group.query.filter_by(id_owner=user_id)
    member_groups = UserGroup.query.filter_by(id_user=user_id)
    groups_list = []
    for group in owner_groups:
        groups_list.append(dicts.create_group_dict(group, None))
    for group in member_groups:
        tmp_group = Group.query.filter_by(id=group.id_group).first()
        groups_list.append(dicts.create_group_dict(tmp_group, None))
    return groups_list


def create_user_events_json(user_id):
    if user_id is None:
        return "Bad request", 400
    events = UserEvent.query.filter_by(id_user=user_id)
    events_list = []
    for event in events:
        tmp_event = Event.query.filter_by(id=event.id_event).first()
        events_list.append(dicts.create_event_dict(tmp_event, None))
    return events_list


def create_movies_json(movie_id):
    if movie_id is None:
        movies = Movie.query.all()
        movies_list = []
        for movie in movies:
            movies_list.append(dicts.create_movie_dict(movie))
        return movies_list
    else:
        movie = Movie.query.filter_by(id=movie_id).first()
        if movie is None:
            return "Not found", 404
        movie_dict = dicts.create_movie_dict(movie)
        return movie_dict


def create_group_json(group_id):
    if group_id is None:
        return "Bad request", 400
    group = Group.query.filter_by(id=group_id).first()
    if group is None:
        return "Not found", 404
    group_members = UserGroup.query.filter_by(id_group=group_id)
    members = []
    for member in group_members:
        user = User.query.filter_by(id=member.id_user).first()
        members.append(dicts.create_user_dict(user))
    group_dict = dicts.create_group_dict(group, members)
    return group_dict


def create_event_json(event_id):
    if event_id is None:
        return "Bad request", 400
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        return "Not found", 404
    event_participators = UserEvent.query.filter_by(id_event=event_id)
    participators = []
    for participator in event_participators:
        user = User.query.filter_by(id=participator.id_user).first()
        participators.append(dicts.create_user_dict(user))
    event_dict = dicts.create_event_dict(event, participators)
    return event_dict


def create_user_json(user_id, swipes, groups, events):
    if user_id is None:
        return "Bad request", 400
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return "Not found", 404
    user_dict = dicts.create_complete_user_dict(user, swipes, groups, events)
    return user_dict
