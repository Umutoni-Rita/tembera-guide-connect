"""
Database connection layer.

This is the ONLY file that talks to SQLite directly.
The services call the small helper functions below (fetch_all, fetch_one,
insert, execute) and never open a connection themselves.
"""

import os
import sqlite3

# Build paths from this file's folder, so the app works from any terminal folder.
DATABASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(DATABASE_FOLDER, "tembera.db")
SCHEMA_PATH = os.path.join(DATABASE_FOLDER, "schema.sql")
SEED_PATH = os.path.join(DATABASE_FOLDER, "seed.sql")


def get_connection():
    """Open a connection to the SQLite database file."""
    connection = sqlite3.connect(DATABASE_PATH)
    # Lets us read columns by name, for example row["full_name"]
    connection.row_factory = sqlite3.Row
    # SQLite does not check foreign keys unless we switch it on
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def run_sql_file(connection, file_path):
    """Run every SQL statement written in a .sql file."""
    with open(file_path, "r", encoding="utf-8") as sql_file:
        connection.executescript(sql_file.read())


def setup_database():
    """Create the tables (if missing) and add sample data the first time.

    Returns True when a brand new database was created.
    """
    is_new_database = not os.path.exists(DATABASE_PATH)
    connection = get_connection()
    try:
        run_sql_file(connection, SCHEMA_PATH)
        if is_new_database:
            run_sql_file(connection, SEED_PATH)
        connection.commit()
    finally:
        connection.close()
    return is_new_database


def reset_database():
    """Delete the database file and rebuild it from schema.sql and seed.sql."""
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    setup_database()


# ---------- Helper functions used by the services ----------

def fetch_all(sql, params=()):
    """Run a SELECT and return a list of rows."""
    connection = get_connection()
    try:
        rows = connection.execute(sql, params).fetchall()
    finally:
        connection.close()
    return rows


def fetch_one(sql, params=()):
    """Run a SELECT and return one row, or None if nothing was found."""
    connection = get_connection()
    try:
        row = connection.execute(sql, params).fetchone()
    finally:
        connection.close()
    return row


def insert(sql, params=()):
    """Run an INSERT and return the ID of the new row."""
    connection = get_connection()
    try:
        cursor = connection.execute(sql, params)
        connection.commit()
        new_id = cursor.lastrowid
    finally:
        connection.close()
    return new_id


def execute(sql, params=()):
    """Run an UPDATE or DELETE and return how many rows were changed."""
    connection = get_connection()
    try:
        cursor = connection.execute(sql, params)
        connection.commit()
        changed_rows = cursor.rowcount
    finally:
        connection.close()
    return changed_rows
