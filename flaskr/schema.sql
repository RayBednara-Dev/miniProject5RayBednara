DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS rounds;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- A round of golf, always owned by the user who logged it in.
CREATE TABLE rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_name TEXT NOT NULL,
    date_played DATE NOT NULL,
    notes TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- One row per player (the logged-in user plus up to 3 friends) per round.
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    round_id INTEGER NOT NULL,
    player_name TEXT NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (round_id) REFERENCES rounds (id)
);
