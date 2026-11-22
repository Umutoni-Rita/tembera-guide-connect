"""
Tour experiences: Create, Read, Update and Delete.
"""

from database.connection import fetch_all, fetch_one, insert, execute
from models.experience import Experience


def row_to_experience(row):
    return Experience(
        row["experience_id"],
        row["name"],
        row["location"],
        row["price_per_person"],
        row["duration_hours"],
    )


def add_experience(experience):
    """Save a new Experience object. Returns the new experience ID."""
    return insert(
        "INSERT INTO experiences (name, location, price_per_person, duration_hours) VALUES (?, ?, ?, ?)",
        (experience.name, experience.location, experience.price_per_person, experience.duration_hours),
    )


def get_all_experiences():
    rows = fetch_all("SELECT * FROM experiences ORDER BY experience_id")
    experiences = []
    for row in rows:
        experiences.append(row_to_experience(row))
    return experiences


def get_experience_by_id(experience_id):
    row = fetch_one("SELECT * FROM experiences WHERE experience_id = ?", (experience_id,))
    if row is None:
        return None
    return row_to_experience(row)


def update_experience(experience):
    return execute(
        "UPDATE experiences SET name = ?, location = ?, price_per_person = ?, duration_hours = ? "
        "WHERE experience_id = ?",
        (experience.name, experience.location, experience.price_per_person,
         experience.duration_hours, experience.experience_id),
    )


def delete_experience(experience_id):
    """Delete an experience. SQLite refuses if it has bookings."""
    return execute("DELETE FROM experiences WHERE experience_id = ?", (experience_id,))
