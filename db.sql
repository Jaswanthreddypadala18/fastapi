CREATE TABLE candidates (
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE,
    phone VARCHAR,
    maths_marks INTEGER,
    history_marks INTEGER
);