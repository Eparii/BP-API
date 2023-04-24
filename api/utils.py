from api import dicts
from api.models import Swipe, Group, UserGroup, Movie, User, Genre, MovieGenre, MovieVoD


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
        groups_list.append(dicts.create_group_dict(group, None, None, None, None))
    for group in member_groups:
        tmp_group = Group.query.filter_by(id=group.id_group).first()
        groups_list.append(dicts.create_group_dict(tmp_group, None, None, None, None))
    return groups_list



def create_movies_json(movie_id, page_num, page_size, group_id, user_id):
    if movie_id is None:
        swiped_movies = Swipe.query.filter_by(id_user=user_id)
        swiped_movies_ids = [swipe.id_movie for swipe in swiped_movies]
        if group_id == "0":  # uzivatel nema vybranou skupinu pro filtrovani
            # vyhledava vsechny filmy s vyjimkou filmu, ktere uzivatel jiz swipnul
            movies = Movie.query.filter(~Movie.id.in_(swiped_movies_ids)).paginate(page=page_num, per_page=page_size)
        else:  # uzivatel vybral skupinu pro filtrovani
            group = Group.query.filter_by(id=group_id).first()
            vod_ids = [vod.id_vod for vod in group.vods]
            genre_ids = [genre.id_genre for genre in group.genres]
            # vrati filmy, ktere uzivatel jeste neswipoval a ktere odpovidaji VoD sluzbam a zanrum ze zvolene skupiny
            movies = Movie.query.filter(~Movie.id.in_(swiped_movies_ids), Movie.vods.any(MovieVoD.id_vod.in_(vod_ids)),
                                        Movie.genres.any(MovieGenre.id_genre.in_(genre_ids))).paginate(page=page_num,
                                                                                                       per_page=page_size)
        movies_list = []
        for movie in movies.items:
            movies_list.append(dicts.create_movie_dict(movie))
        return {
            "movies": movies_list,
            "current_page": movies.page,
            "total_pages": movies.pages,
            "total_items": movies.total,
        }
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
    owner = User.query.filter_by(id=group.id_owner).first()

    vod_ids = [vod.id_vod for vod in group.vods]
    genre_ids = [genre.id_genre for genre in group.genres]
    matches_ids = []
    members = []
    genres = []
    vods = []

    for swipe in owner.swipes:
        if swipe.type == 'like':
            matches_ids.append(swipe.id_movie)
    for member in group_members:
        user = User.query.filter_by(id=member.id_user).first()
        likes = []
        for swipe in user.swipes:
            if swipe.type == 'like':
                likes.append(swipe.movie.id)
        for match in matches_ids:
            if match not in likes:
                matches_ids.remove(match)
        members.append(dicts.create_user_dict(user))

    matches = [movie.id for movie in Movie.query.filter(Movie.id.in_(matches_ids),
                                                        Movie.vods.any(MovieVoD.id_vod.in_(vod_ids)),
                                                        Movie.genres.any(MovieGenre.id_genre.in_(genre_ids)))]

    for genre in group.genres:
        genres.append(genre.id_genre)
    for vod in group.vods:
        vods.append(vod.id_vod)

    group_dict = dicts.create_group_dict(group, members, matches, genres, vods)
    return group_dict


def create_user_json(user_id, swipes, groups):
    if user_id is None:
        return "Bad request", 400
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return "Not found", 404
    user_dict = dicts.create_complete_user_dict(user, swipes, groups)
    return user_dict
