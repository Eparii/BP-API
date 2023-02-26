from time import strftime

from api.models import MovieGenre, Genre, User


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
        "id": swipe.id,
        "movie": swipe.id_movie,
        "type": swipe.type,
    }
    return swipe_dict


def create_group_dict(group, members):
    owner = User.query.filter_by(id=group.id_owner).first()
    owner = create_user_dict(owner)
    if members is not None:
        group_dict = {
            "id": group.id,
            "name": group.name,
            "owner": owner,
            "members": members
        }
    else:
        group_dict = {
            "id": group.id,
            "owner": owner,
            "name": group.name,
        }
    return group_dict


def create_event_dict(event, participators):
    if participators is not None:
        event_dict = {
            "id": event.id,
            "start": event.start.strftime("%d/%m/%Y, %H:%M:%S"),
            "description": event.description,
            "participators": participators
        }
    else:
        event_dict = {
            "id": event.id,
            "start": event.start.strftime("%d/%m/%Y, %H:%M:%S"),
            "description": event.description,
        }
    return event_dict


def create_movie_dict(movie):
    genres = []
    movie_genres = MovieGenre.query.filter_by(id_movie=movie.id)
    for movie_genre in movie_genres:
        genre = Genre.query.filter_by(id=movie_genre.id_genre).first()
        genres.append(genre.name)
    movie_dict = {
        "id": movie.id,
        "name": movie.name,
        "release_year": movie.release_year,
        "IMDB_rating": movie.IMDB_rating,
        "image_url": movie.image_url,
        "description": movie.description,
        "genres": genres
    }
    return movie_dict


def create_complete_user_dict(user, swipes, groups, events):
    user_dict = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "swipes": swipes,
        "groups": groups,
        "events": events
    }
    return user_dict
