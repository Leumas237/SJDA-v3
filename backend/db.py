"""Accès PostgreSQL : schéma et helpers."""
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from .config import DATABASE_URL

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            BIGSERIAL PRIMARY KEY,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt          TEXT NOT NULL,
    name          TEXT NOT NULL,
    is_admin      INTEGER NOT NULL DEFAULT 0,
    banned        INTEGER NOT NULL DEFAULT 0,
    approved      INTEGER NOT NULL DEFAULT 0,
    last_seen     TIMESTAMPTZ NOT NULL DEFAULT 'epoch',
    spam_strikes  INTEGER NOT NULL DEFAULT 0,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS profiles (
    user_id   BIGINT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    bio       TEXT NOT NULL DEFAULT '',
    classe    TEXT NOT NULL DEFAULT '',
    interests TEXT NOT NULL DEFAULT '[]',
    intent    TEXT NOT NULL DEFAULT 'les_deux',
    gender    TEXT NOT NULL DEFAULT '',
    seeking   TEXT NOT NULL DEFAULT 'tous',
    photo     TEXT NOT NULL DEFAULT '',
    instagram TEXT NOT NULL DEFAULT '',
    snapchat  TEXT NOT NULL DEFAULT '',
    whatsapp  TEXT NOT NULL DEFAULT '',
    age       INTEGER NOT NULL DEFAULT 0,
    invisible INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sessions (
    token      TEXT PRIMARY KEY,
    user_id    BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS swipes (
    swiper_id  BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_id  BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    liked      INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (swiper_id, target_id)
);

CREATE TABLE IF NOT EXISTS matches (
    id         BIGSERIAL PRIMARY KEY,
    user_a     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_b     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    closed     INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_a, user_b)
);

CREATE TABLE IF NOT EXISTS reports (
    id          BIGSERIAL PRIMARY KEY,
    reporter_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reported_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    match_id    BIGINT REFERENCES matches(id) ON DELETE SET NULL,
    reason      TEXT NOT NULL DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'pending',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS kyi (
    user_id      BIGINT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    full_name    TEXT NOT NULL DEFAULT '',
    birthdate    TEXT NOT NULL DEFAULT '',
    classe       TEXT NOT NULL DEFAULT '',
    card_photo   TEXT NOT NULL DEFAULT '',
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS photos (
    id       BIGSERIAL PRIMARY KEY,
    user_id  BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    position INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_photos_user ON photos(user_id, position, id);

CREATE TABLE IF NOT EXISTS push_subs (
    endpoint TEXT PRIMARY KEY,
    user_id  BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sub      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS activity (
    id         BIGSERIAL PRIMARY KEY,
    type       TEXT NOT NULL,
    text       TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db() -> None:
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL (or SJDA_DATABASE_URL) must be set for PostgreSQL"
        )
    with get_db() as db:
        for statement in SCHEMA.split(";"):
            statement = statement.strip()
            if statement:
                db.execute(statement)


@contextmanager
def get_db():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL (or SJDA_DATABASE_URL) must be set for PostgreSQL"
        )
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        yield conn
