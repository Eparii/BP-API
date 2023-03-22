DROP TABLE IF EXISTS user_t CASCADE;
DROP TABLE IF EXISTS swipe_t CASCADE;
-- DROP TABLE IF EXISTS movie_t CASCADE;
DROP TABLE IF EXISTS group_t CASCADE;
DROP TABLE IF EXISTS genre_t CASCADE;
DROP TABLE IF EXISTS event_t CASCADE;
DROP TABLE IF EXISTS event_movie_t CASCADE;
DROP TABLE IF EXISTS user_event_t CASCADE;
DROP TABLE IF EXISTS user_group_t CASCADE;
DROP TABLE IF EXISTS movie_genre_t CASCADE;
DROP TABLE IF EXISTS vod_t CASCADE;
DROP TABLE IF EXISTS movie_vod_t CASCADE;
DROP TYPE IF EXISTS SWIPE_TYPE;

CREATE TYPE SWIPE_TYPE AS ENUM ('like', 'dislike', 'skip');

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
    password_hash VARCHAR(60) NOT NULL
);

CREATE TABLE movie_t
(
    id_movie SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    release_year INT NOT NULL,
    image_url VARCHAR(512) NOT NULL,
    rating FLOAT,
    description VARCHAR(2048) NOT NULL
);

CREATE TABLE swipe_t
(
    id_swipe SERIAL PRIMARY KEY,
    type SWIPE_TYPE NOT NULL,

    id_user INT REFERENCES user_t(id_user) ON DELETE CASCADE,
    id_movie INT REFERENCES movie_t(id_movie) ON DELETE CASCADE
);

CREATE TABLE genre_t
(
    id_genre SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

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


CREATE TABLE movie_genre_t
(
    id_movie INT REFERENCES movie_t(id_movie) ON DELETE CASCADE,
    id_genre INT REFERENCES genre_t(id_genre) ON DELETE CASCADE,

    PRIMARY KEY (id_movie, id_genre)
);

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

INSERT INTO user_t (firstname, lastname, email, password_hash) VALUES
    ('Pavel', 'Růžička', 'pavel.ruzicka@seznam.cz', '$2a$12$xmsFeYG4cnm7BIcXwNPNLulL/TrehULqhuwortGOR3AfPidTeVI4y'),
    ('Gustav', 'Svoboda', 'gustav.svoboda@seznam.cz', '$2b$12$xmsFeYG4cnm7BIcXwNPNLulL/TrehULqhuwortGOR3AfPidTeVI4y'),
    ('Alexandr', 'Veliký', 'alex.big@seznam.cz', '$2c$12$xmsFeYG4cnm7BIcXwNPNLulL/TrehULqhuwortGOR3AfPidTeVI4y');

-- INSERT INTO movie_t (name, release_year, image_url, rating, description) VALUES
--    ('Interstellar', 2014, 'https://static.posters.cz/image/750/plakaty/interstellar-ice-walk-i23290.jpg', 8.6, 'The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.'),
--    ('Avatar', 2009, 'https://static.posters.cz/image/750/plakaty/avatar-limited-ed-one-sheet-sun-i7182.jpg', 7.8, 'In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.'),
--    ('How to Train Your Dragon: The Hidden World', 2019, 'https://www.themoviedb.org/t/p/original/xvx4Yhf0DVH8G4LzNISpMfFBDy2.jpg', 7.8, 'As Hiccup fulfills his dream of creating a peaceful dragon utopia, Toothless’ discovery of an untamed, elusive mate draws the Night Fury away. When danger mounts at home and Hiccup’s reign as village chief is tested, both dragon and rider must make impossible decisions to save their kind.'),
--   ('Top Gun', 1986, 'https://www.themoviedb.org/t/p/original/xUuHj3CgmZQ9P2cMaqQs4J0d4Zc.jpg', 6.9, 'For Lieutenant Pete ''Maverick'' Mitchell and his friend and co-pilot Nick ''Goose'' Bradshaw, being accepted into an elite training school for fighter pilots is a dream come true. But a tragedy, as well as personal demons, will threaten Pete''s dreams of becoming an ace pilot.'),
--   ('How to Train Your Dragon', 2010, 'https://www.themoviedb.org/t/p/original/ygGmAO60t8GyqUo9xYeYxSZAR3b.jpg', 7.8, 'As the son of a Viking leader on the cusp of manhood, shy Hiccup Horrendous Haddock III faces a rite of passage: he must kill a dragon to prove his warrior mettle. But after downing a feared dragon, he realizes that he no longer wants to destroy it, and instead befriends the beast – which he names Toothless – much to the chagrin of his warrior father.'),
--    ('Avengers: Infinity War', 2018, 'https://www.themoviedb.org/t/p/original/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg', 8.3, 'As the Avengers and their allies have continued to protect the world from threats too large for any one hero to handle, a new danger has emerged from the cosmic shadows: Thanos. A despot of intergalactic infamy, his goal is to collect all six Infinity Stones, artifacts of unimaginable power, and use them to inflict his twisted will on all of reality. Everything the Avengers have fought for has led up to this moment - the fate of Earth and existence itself has never been more uncertain.'),
--    ('Once Upon a Time in the West', 1968, 'https://www.themoviedb.org/t/p/original/qbYgqOczabWNn2XKwgMtVrntD6P.jpg', 8.3, 'As the railroad builders advance unstoppably through the Arizona desert on their way to the sea, Jill arrives in the small town of Flagstone with the intention of starting a new life.'),
--    ('#FriendButMarried', 2018, 'https://www.themoviedb.org/t/p/original/splV83B3CqMCbHUunoyaUoRUM60.jpg', 6.8, 'Pining for his high school crush for years, a young man puts up his best efforts to move out of the friend zone until she reveals she''s getting married.');

--
-- INSERT INTO swipe_t (type, id_user, id_movie) VALUES
--     ('like', 1, 2), ('like', 1, 3),
--     ('dislike', 1, 4), ('dislike', 1, 5), ('like', 1, 6),
--   ('like', 2, 2), ('dislike', 2, 3),
--   ('like', 3, 1), ('like', 3, 3);

INSERT INTO genre_t (id_genre, name) VALUES
    (28, 'Action'), (12, 'Adventure'), (16, 'Animation'),
    (35, 'Comedy'), (80, 'Crime'), (99, 'Documentary'),
    (18, 'Drama'), (10751, 'Family'), (14, 'Fantasy'),
    (36, 'History'), (27, 'Horror'), (10402, 'Music'),
    (9648, 'Mystery'), (10749, 'Romance'), (878, 'Science Fiction'),
    (10770, 'TV Movie'), (53, 'Thriller'), (10752, 'War'), (37, 'Western');


-- INSERT INTO movie_genre_t (id_movie, id_genre) VALUES
--     (1, 2), (2, 2), (3, 3);

INSERT INTO vod_t(name) VALUES
    ('Netflix'), ('Disney+');


INSERT INTO group_t (id_owner, name) VALUES
    (1, 'Borci');

INSERT INTO user_group_t (id_user, id_group) VALUES
    (2, 1), (3, 1);

-- INSERT INTO event_t (start, description, id_group, id_chosen_movie) VALUES
--     (timestamp '2023-07-20 10:00:00', 'prijďte včas', 1, 1);
--
-- INSERT INTO user_event_t (id_user, id_event) VALUES
--     (2, 1), (3, 1)

select * from movie_genre_t;
