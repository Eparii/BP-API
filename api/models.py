from api import db


class User(db.Model):
    __tablename__ = 'user_t'
    id = db.Column('id_user', db.Integer, primary_key=True)
    first_name = db.Column('firstname', db.String(50), nullable=False)
    last_name = db.Column('lastname', db.String(50), nullable=False)
    email = db.Column('email', db.String(255), nullable=False, unique=True)
    password_hash = db.Column('password_hash', db.String(60), nullable=False)

    member_groups = db.relationship('Group', cascade='all, delete-orphan', backref='member', lazy=True)
    owner_groups = db.relationship('UserGroup', cascade='all, delete-orphan', backref='owner', lazy=True)
    swipes = db.relationship('Swipe', cascade='all, delete-orphan', backref='user', lazy=True)
    events_participating = db.relationship('UserEvent', cascade='all, delete-orphan', backref='participant', lazy=True)


class Movie(db.Model):
    __tablename__ = 'movie_t'
    id = db.Column('id_movie', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255), nullable=False)
    release_year = db.Column('release_year', db.Integer, nullable=False)
    image_url = db.Column('image_url', db.String(512), nullable=False)
    rating = db.Column('rating', db.Float, nullable=False)
    description = db.Column('description', db.String(2048), nullable=False)
    tmdb_id = db.Column('tmdb_id', db.Integer, nullable=False)

    events_listed = db.relationship('EventMovie', cascade='all, delete-orphan', backref='listed_movie', lazy=True)
    events_chosen = db.relationship('Event', cascade='all, delete-orphan', backref='chosen_movie', lazy=True)
    swipes = db.relationship('Swipe', cascade='all, delete-orphan', backref='movie', lazy=True)
    genres = db.relationship('MovieGenre', cascade='all, delete-orphan', backref='movie', lazy=True)
    vods = db.relationship('MovieVoD', cascade='all, delete-orphan', backref='movie', lazy=True)


class Swipe(db.Model):
    __tablename__ = 'swipe_t'
    id = db.Column('id_swipe', db.Integer, primary_key=True)
    type = db.Column('type', db.Enum('like', 'dislike', 'skip'), nullable=False)

    id_user = db.Column(db.Integer, db.ForeignKey('user_t.id_user'), nullable=False)
    id_movie = db.Column(db.Integer, db.ForeignKey('movie_t.id_movie'), nullable=False)


class Genre(db.Model):
    __tablename__ = 'genre_t'
    id = db.Column('id_genre', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False)

    movies = db.relationship('MovieGenre', cascade='all, delete-orphan', backref='genre', lazy=True)
    groups = db.relationship('GroupGenre', cascade='all, delete-orphan', backref='genre', lazy=True)


class Group(db.Model):
    __tablename__ = 'group_t'
    id = db.Column('id_group', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False)

    id_owner = db.Column(db.Integer, db.ForeignKey('user_t.id_user'), nullable=False)
    members = db.relationship('UserGroup', cascade='all, delete-orphan', backref='group', lazy=True)
    genres = db.relationship('GroupGenre', cascade='all, delete-orphan', backref='group', lazy=True)


class Event(db.Model):
    __tablename__ = 'event_t'
    id = db.Column('id_event', db.Integer, primary_key=True)
    start = db.Column('start', db.DateTime, nullable=False)
    description = db.Column('description', db.String(255), nullable=True)

    id_group = db.Column(db.Integer, db.ForeignKey('group_t.id_group'), nullable=False)
    id_chosen_movie = db.Column(db.Integer, db.ForeignKey('movie_t.id_movie'), nullable=True)
    participants = db.relationship('UserEvent', cascade='all, delete-orphan', backref='event', lazy=True)
    movies_listed = db.relationship('EventMovie', cascade='all, delete-orphan', backref='event', lazy=True)


class VoD(db.Model):
    __tablename__ = 'vod_t'
    id = db.Column('id_vod', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))

    movies_available = db.relationship('MovieVoD', cascade='all, delete-orphan', backref='VoD', lazy=True)


class MovieVoD(db.Model):
    __tablename__ = 'movie_vod_t'
    id_movie = db.Column(db.Integer, db.ForeignKey('movie_t.id_movie'), primary_key=True)
    id_vod = db.Column(db.Integer, db.ForeignKey('vod_t.id_vod'), primary_key=True)


class MovieGenre(db.Model):
    __tablename__ = 'movie_genre_t'
    id_movie = db.Column(db.Integer, db.ForeignKey('movie_t.id_movie'), primary_key=True)
    id_genre = db.Column(db.Integer, db.ForeignKey('genre_t.id_genre'), primary_key=True)


class UserGroup(db.Model):
    __tablename__ = 'user_group_t'
    id_user = db.Column(db.Integer, db.ForeignKey('user_t.id_user'), primary_key=True)
    id_group = db.Column(db.Integer, db.ForeignKey('group_t.id_group'), primary_key=True)


class UserEvent(db.Model):
    __tablename__ = 'user_event_t'
    id_user = db.Column(db.Integer, db.ForeignKey('user_t.id_user'), primary_key=True)
    id_event = db.Column(db.Integer, db.ForeignKey('event_t.id_event'), primary_key=True)


class EventMovie(db.Model):
    __tablename__ = 'event_movie_t'
    id_event = db.Column(db.Integer, db.ForeignKey('event_t.id_event'), primary_key=True)
    id_movie = db.Column(db.Integer, db.ForeignKey('movie_t.id_movie'), primary_key=True)


class GroupGenre(db.Model):
    __tablename__ = 'group_genre_t'
    id_genre = db.Column(db.Integer, db.ForeignKey('genre_t.id_genre'), primary_key=True)
    id_group = db.Column(db.Integer, db.ForeignKey('group_t.id_group'), primary_key=True)
