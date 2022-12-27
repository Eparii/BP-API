def create_user_dict(user):
    user_dict = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }
    return user_dict


def create_swipe_dict(swipe):
    swipe_dict = {
        "movie": swipe.id_movie,
        "type": swipe.type,
    }
    return swipe_dict


def create_group_dict(group):
    group_dict = {
        "name": group.name
    }
    return group_dict
