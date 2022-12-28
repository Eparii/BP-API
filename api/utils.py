from api import dicts
from api.models import Swipe, Group, UserGroup, UserEvent, Event, Movie, User


def create_user_swipes_json(user_id, swipes_type):
    if swipes_type is None:
        return "Bad request", 400
    swipes = Swipe.query.filter_by(id_user=user_id, type=swipes_type)
    swipes_list = []
    for swipe in swipes:
        swipes_list.append(dicts.create_swipe_dict(swipe))
    return swipes_list


def create_user_groups_json(user_id):
    owner_groups = Group.query.filter_by(id_owner=user_id)
    member_groups = UserGroup.query.filter_by(id_user=user_id)
    groups_list = []
    for group in owner_groups:
        groups_list.append(dicts.create_group_dict(group))
    for group in member_groups:
        tmp_group = Group.query.filter_by(id=group.id).first()
        groups_list.append(dicts.create_group_dict(tmp_group))

    return groups_list


def create_user_events_json(user_id):
    events = UserEvent.query.filter_by(id_user=user_id)
    events_list = []
    for event in events:
        tmp_event = Event.query.filter_by(id=event.id).first()
        participators = []
        event_participators = UserEvent.query.filter_by(id_event=tmp_event.id)
        for participator in event_participators:
            user = User.query.filter_by(id=participator.id_user).first()
            participators.append(dicts.create_user_dict(user))
        events_list.append(dicts.create_event_dict(tmp_event, participators))
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
        movie_dict = dicts.create_movie_dict(movie)
        return movie_dict


def create_group_json(group_id):
    if group_id is None:
        return "Bad request", 400
    group = Group.query.filter_by(id=group_id).first()
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
    event_participators = UserEvent.query.filter_by(id_event=event_id)
    participators = []
    for participator in event_participators:
        user = User.query.filter_by(id=participator.id_user).first()
        participators.append(dicts.create_user_dict(user))
    event_dict = dicts.create_event_dict(event, participators)
    return event_dict
