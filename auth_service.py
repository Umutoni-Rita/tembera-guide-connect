"""
User accounts: login, creating accounts (register), and managing them.
"""

import hashlib

from database.connection import fetch_all, fetch_one, insert, execute
from models.user import User


def hash_password(password):
    """Turn a password into a SHA-256 hash so we never store the real password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def row_to_user(row):
    return User(row["user_id"], row["username"], row["full_name"], row["role"])


def login(username, password):
    """Return the User if the username and password match, otherwise None."""
    row = fetch_one(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username, hash_password(password)),
    )
    if row is None:
        return None
    return row_to_user(row)


def create_user(username, password, full_name, role):
    """Register a new account. Returns the new user ID."""
    return insert(
        "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
        (username, hash_password(password), full_name, role),
    )


def get_all_users():
    rows = fetch_all("SELECT * FROM users ORDER BY user_id")
    users = []
    for row in rows:
        users.append(row_to_user(row))
    return users


def get_user_by_id(user_id):
    row = fetch_one("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if row is None:
        return None
    return row_to_user(row)


def update_user(user_id, full_name, role):
    return execute(
        "UPDATE users SET full_name = ?, role = ? WHERE user_id = ?",
        (full_name, role, user_id),
    )


def reset_password(user_id, new_password):
    return execute(
        "UPDATE users SET password_hash = ? WHERE user_id = ?",
        (hash_password(new_password), user_id),
    )


def delete_user(user_id):
    return execute("DELETE FROM users WHERE user_id = ?", (user_id,))
