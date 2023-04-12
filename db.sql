DROP TABLE IF EXISTS user_t CASCADE;
DROP TABLE IF EXISTS swipe_t CASCADE;
-- DROP TABLE IF EXISTS movie_t CASCADE;
DROP TABLE IF EXISTS group_t CASCADE;
-- DROP TABLE IF EXISTS genre_t CASCADE;
DROP TABLE IF EXISTS event_t CASCADE;
DROP TABLE IF EXISTS event_movie_t CASCADE;
DROP TABLE IF EXISTS user_event_t CASCADE;
DROP TABLE IF EXISTS user_group_t CASCADE;
-- DROP TABLE IF EXISTS movie_genre_t CASCADE;
DROP TABLE IF EXISTS vod_t CASCADE;
DROP TABLE IF EXISTS movie_vod_t CASCADE;
DROP TABLE IF EXISTS group_genre_t CASCADE;
DROP TABLE IF EXISTS group_vod_t CASCADE;
DROP TYPE IF EXISTS SWIPE_TYPE;

CREATE TYPE SWIPE_TYPE AS ENUM ('like', 'dislike', 'seen');

CREATE TABLE vod_t
(
    id_vod SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE user_t
(
    id_user SERIAL PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(64) NOT NULL
);

-- CREATE TABLE movie_t
-- (
--     id_movie SERIAL PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     release_year INT NOT NULL,
--     image_url VARCHAR(512) NOT NULL,
--     rating FLOAT NOT NULL,
--     tmdb_id INT NOT NULL,
--     description VARCHAR(2048) NOT NULL
-- );

CREATE TABLE swipe_t
(
    id_swipe SERIAL PRIMARY KEY,
    type SWIPE_TYPE NOT NULL,

    id_user INT REFERENCES user_t(id_user) ON DELETE CASCADE,
    id_movie INT REFERENCES movie_t(id_movie) ON DELETE CASCADE
);
--
-- CREATE TABLE genre_t
-- (
--     id_genre SERIAL PRIMARY KEY,
--     name VARCHAR(50) NOT NULL
-- );

CREATE TABLE group_t
(
    id_group SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,

    id_owner INT REFERENCES user_t(id_user) ON DELETE SET NULL
);

CREATE TABLE event_t
(
    id_event SERIAL PRIMARY KEY,
    start TIMESTAMP NOT NULL,
    description VARCHAR(255),

    id_group INT REFERENCES group_t(id_group),
    id_chosen_movie INT REFERENCES movie_t(id_movie)
);


-- CREATE TABLE movie_genre_t
-- (
--     id_movie INT REFERENCES movie_t(id_movie) ON DELETE CASCADE,
--     id_genre INT REFERENCES genre_t(id_genre) ON DELETE CASCADE,
--
--     PRIMARY KEY (id_movie, id_genre)
-- );

CREATE TABLE user_group_t
(
    id_user INT REFERENCES user_t(id_user) ON DELETE CASCADE,
    id_group INT REFERENCES group_t(id_group) ON DELETE CASCADE,

    PRIMARY KEY (id_user, id_group)
);

CREATE TABLE event_movie_t
(
    id_event INT REFERENCES event_t(id_event) ON DELETE CASCADE,
    id_movie INT REFERENCES movie_t(id_movie) ON DELETE CASCADE,

    PRIMARY KEY(id_event, id_movie)
);

CREATE TABLE user_event_t
(
    id_user INT REFERENCES user_t(id_user) ON DELETE CASCADE,
    id_event INT REFERENCES event_t(id_event) ON DELETE CASCADE,

    PRIMARY KEY(id_user, id_event)
);

CREATE TABLE movie_vod_t
(
    id_vod INT REFERENCES vod_t(id_vod) ON DELETE CASCADE,
    id_movie INT REFERENCES movie_t(id_movie) ON DELETE CASCADE,

    PRIMARY KEY(id_vod, id_movie)
);

CREATE TABLE group_genre_t
(
    id_group INT REFERENCES group_t(id_group) ON DELETE CASCADE,
    id_genre INT REFERENCES genre_t(id_genre) ON DELETE CASCADE,

    PRIMARY KEY(id_group, id_genre)
);

CREATE TABLE group_vod_t
(
    id_group INT REFERENCES group_t(id_group) ON DELETE CASCADE,
    id_vod INT REFERENCES vod_t(id_vod) ON DELETE CASCADE,

    PRIMARY KEY(id_group, id_vod)
);

INSERT INTO user_t (firstname, lastname, email, password_hash) VALUES
    ('Pavel', 'Růžička', 'pavel.ruzicka@seznam.cz', '$2a$12$xmsFeYG4cnm7BIcXwNPNLulL/TrehULqhuwortGOR3AfPidTeVI4y'),
    ('Gustav', 'Svoboda', 'gustav.svoboda@seznam.cz', '$2b$12$xmsFeYG4cnm7BIcXwNPNLulL/TrehULqhuwortGOR3AfPidTeVI4y'),
    ('Alexandr', 'Veliký', 'alex.big@seznam.cz', '$2c$12$xmsFeYG4cnm7BIcXwNPNLulL/TrehULqhuwortGOR3AfPidTeVI4y');

-- INSERT INTO genre_t (id_genre, name) VALUES
--     (28, 'Action'), (12, 'Adventure'), (16, 'Animation'),
--     (35, 'Comedy'), (80, 'Crime'), (99, 'Documentary'),
--     (18, 'Drama'), (10751, 'Family'), (14, 'Fantasy'),
--     (36, 'History'), (27, 'Horror'), (10402, 'Music'),
--     (9648, 'Mystery'), (10749, 'Romance'), (878, 'Sci-Fi'),
--     (10770, 'TV Movie'), (53, 'Thriller'), (10752, 'War'), (37, 'Western');


INSERT INTO vod_t(name) VALUES
    ('Netflix'), ('Disney+');


INSERT INTO group_t (id_owner, name) VALUES
    (1, 'Borci');

INSERT INTO user_group_t (id_user, id_group) VALUES
    (2, 1);

INSERT INTO swipe_t(type, id_user, id_movie) VALUES
    ('like', 2, 1), ('like', 2, 2), ('dislike', 2, 3),
    ('like', 2, 4),('like', 2, 5), ('dislike', 2, 6);

-- INSERT INTO event_t (start, description, id_group, id_chosen_movie) VALUES
--     (timestamp '2023-07-20 10:00:00', 'prijďte včas', 1, 1);
--
-- INSERT INTO user_event_t (id_user, id_event) VALUES
--     (2, 1), (3, 1)
select * from user_t;