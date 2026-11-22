-- ============================================================
-- Tembera Guide Connect - database schema (SQLite)
-- This file can rebuild the whole database from scratch.
-- ============================================================

-- People who can log in to the app.
-- role decides which menu they see: 'admin' or 'coordinator'.
CREATE TABLE IF NOT EXISTS users (
    user_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    username       TEXT NOT NULL UNIQUE,
    password_hash  TEXT NOT NULL,
    full_name      TEXT NOT NULL,
    role           TEXT NOT NULL CHECK (role IN ('admin', 'coordinator'))
);

-- Local guides of the cooperative.
-- languages is saved as text like 'EN,FR,KIN'.
CREATE TABLE IF NOT EXISTS guides (
    guide_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name  TEXT NOT NULL,
    phone      TEXT NOT NULL UNIQUE,
    gender     TEXT NOT NULL CHECK (gender IN ('F', 'M')),
    languages  TEXT NOT NULL
);

-- Tour experiences that tourists can book.
CREATE TABLE IF NOT EXISTS experiences (
    experience_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name              TEXT NOT NULL UNIQUE,
    location          TEXT NOT NULL,
    price_per_person  INTEGER NOT NULL CHECK (price_per_person > 0),
    duration_hours    REAL NOT NULL CHECK (duration_hours > 0)
);

-- One row per tourist booking.
-- A guide or experience that has bookings cannot be deleted (RESTRICT).
-- If the user who made the booking is deleted, created_by becomes empty (SET NULL).
CREATE TABLE IF NOT EXISTS bookings (
    booking_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    tourist_name     TEXT NOT NULL,
    group_size       INTEGER NOT NULL CHECK (group_size > 0),
    tour_date        TEXT NOT NULL,
    language         TEXT NOT NULL,
    experience_id    INTEGER NOT NULL,
    guide_id         INTEGER NOT NULL,
    total_price      INTEGER NOT NULL,
    community_share  INTEGER NOT NULL,
    status           TEXT NOT NULL DEFAULT 'confirmed'
                     CHECK (status IN ('confirmed', 'cancelled')),
    created_by       INTEGER,
    FOREIGN KEY (experience_id) REFERENCES experiences (experience_id) ON DELETE RESTRICT,
    FOREIGN KEY (guide_id)      REFERENCES guides (guide_id)           ON DELETE RESTRICT,
    FOREIGN KEY (created_by)    REFERENCES users (user_id)             ON DELETE SET NULL
);
