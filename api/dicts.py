from time import strftime

from api.models import MovieGenre, Genre, User, VoD, MovieVoD


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


def create_group_dict(group, members, matches, genres, vods):
    owner = User.query.filter_by(id=group.id_owner).first()
    owner = create_user_dict(owner)
    if members is not None:
        group_dict = {
            "id": group.id,
            "name": group.name,
            "owner": owner,
            "group_code": group.group_code,
            "members": members,
            "matches": matches,
            "genres": genres,
            "vods": vods
        }
    else:
        group_dict = {
            "id": group.id,
            "owner": owner,
            "name": group.name,
        }
    return group_dict


def create_movie_dict(movie):
    genres = []
    vods = []
    movie_genres = MovieGenre.query.filter_by(id_movie=movie.id)
    movie_vods = MovieVoD.query.filter_by(id_movie=movie.id)
    for movie_genre in movie_genres:
        genre = Genre.query.filter_by(id=movie_genre.id_genre).first()
        genres.append(genre.name)
    for movie_vod in movie_vods:
        vod = VoD.query.filter_by(id=movie_vod.id_vod).first()
        vods.append(vod.name)
    movie_dict = {
        "id": movie.id,
        "name": movie.name,
        "release_year": movie.release_year,
        "rating": movie.rating,
        "image_url": movie.image_url,
        "description": movie.description,
        "tmdb_id": movie.tmdb_id,
        "genres": genres,
        "vods": vods
    }
    return movie_dict


def create_complete_user_dict(user, swipes, groups):
    user_dict = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "swipes": swipes,
        "groups": groups
    }
    return user_dict
