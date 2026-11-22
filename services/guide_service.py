"""
Guides: Create, Read, Update and Delete.
"""

from database.connection import fetch_all, fetch_one, insert, execute
from models.guide import Guide


def row_to_guide(row):
    """Turn a database row into a Guide object."""
    languages = row["languages"].split(",")
    return Guide(row["guide_id"], row["full_name"], row["phone"], row["gender"], languages)


def add_guide(guide):
    """Save a new Guide object. Returns the new guide ID."""
    return insert(
        "INSERT INTO guides (full_name, phone, gender, languages) VALUES (?, ?, ?, ?)",
        (guide.full_name, guide.phone, guide.gender, guide.languages_text()),
    )


def get_all_guides():
    rows = fetch_all("SELECT * FROM guides ORDER BY guide_id")
    guides = []
    for row in rows:
        guides.append(row_to_guide(row))
    return guides


def get_guide_by_id(guide_id):
    row = fetch_one("SELECT * FROM guides WHERE guide_id = ?", (guide_id,))
    if row is None:
        return None
    return row_to_guide(row)


def update_guide(guide):
    """Save the changed details of an existing Guide object."""
    return execute(
        "UPDATE guides SET full_name = ?, phone = ?, gender = ?, languages = ? WHERE guide_id = ?",
        (guide.full_name, guide.phone, guide.gender, guide.languages_text(), guide.guide_id),
    )


def delete_guide(guide_id):
    """Delete a guide. SQLite refuses if the guide has bookings."""
    return execute("DELETE FROM guides WHERE guide_id = ?", (guide_id,))
