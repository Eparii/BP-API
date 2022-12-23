def create_user_dict(user):
    restaurant_dict = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }
    return restaurant_dict
