from api import dicts
from api.models import Swipe, Group, UserGroup, UserEvent, Event


def create_swipes_json(user_id, swipes_type):
    swipes = Swipe.query.filter_by(id_user=user_id, type=swipes_type)
    swipes_list = []
    for swipe in swipes:
        swipes_list.append(dicts.create_swipe_dict(swipe))
    return swipes_list


def create_groups_json(user_id):
    owner_groups = Group.query.filter_by(id_owner=user_id)
    member_groups = UserGroup.query.filter_by(id_user=user_id)
    groups_list = []
    for group in owner_groups:
        groups_list.append(dicts.create_group_dict(group))
    for group in member_groups:
        groups_list.append(Group.query.filter_by(id=group.id).first())

    return groups_list


def create_events_json(user_id):
    events = UserEvent.query.filter_by(id_user=user_id)
    events_list = []
    for event in events:
        events_list.append(Event.query.filter_by(id=event.id).first())
    return events_list
