"""
Bookings
"""

from database.connection import fetch_all, fetch_one, insert, execute
from models.booking import Booking
from services.guide_service import get_all_guides
from services.experience_service import get_experience_by_id

# 10% of every booking goes to the community fund
COMMUNITY_SHARE_PERCENT = 10

# One SELECT used by every "read bookings" function.
# LEFT JOIN on users so a booking still shows if its creator was deleted.
BOOKING_SELECT = """
    SELECT b.*, e.name AS experience_name, g.full_name AS guide_name,
           u.username AS booked_by
    FROM bookings b
    JOIN experiences e ON b.experience_id = e.experience_id
    JOIN guides g ON b.guide_id = g.guide_id
    LEFT JOIN users u ON b.created_by = u.user_id
"""


def row_to_booking(row):
    booked_by = row["booked_by"]
    if booked_by is None:
        booked_by = "-"
    return Booking(
        row["booking_id"], row["tourist_name"], row["group_size"], row["tour_date"],
        row["language"], row["experience_id"], row["guide_id"], row["total_price"],
        row["community_share"], row["status"],
        row["experience_name"], row["guide_name"], booked_by,
    )


def rows_to_bookings(rows):
    bookings = []
    for row in rows:
        bookings.append(row_to_booking(row))
    return bookings


def calculate_community_share(total_price):
    return total_price * COMMUNITY_SHARE_PERCENT // 100


# ---------- Fair guide selection ----------

def guide_is_busy(guide_id, tour_date):
    """True if the guide already has a confirmed booking on that date."""
    row = fetch_one(
        "SELECT COUNT(*) AS total FROM bookings "
        "WHERE guide_id = ? AND tour_date = ? AND status = 'confirmed'",
        (guide_id, tour_date),
    )
    return row["total"] > 0


def count_tours_in_month(guide_id, month):
    """How many confirmed tours the guide has in a month like '2026-11'."""
    row = fetch_one(
        "SELECT COUNT(*) AS total FROM bookings "
        "WHERE guide_id = ? AND tour_date LIKE ? AND status = 'confirmed'",
        (guide_id, month + "%"),
    )
    return row["total"]


def get_guide_workload(tour_date):
    """For the month of tour_date, return {guide_id: (tours_in_month, busy_that_day)}.

    One query for all guides (instead of two queries per guide).
    Only confirmed bookings count.
    """
    rows = fetch_all(
        "SELECT guide_id, COUNT(*) AS tours, "
        "SUM(CASE WHEN tour_date = ? THEN 1 ELSE 0 END) AS on_day "
        "FROM bookings WHERE status = 'confirmed' AND tour_date LIKE ? "
        "GROUP BY guide_id",
        (tour_date, tour_date[:7] + "%"),
    )
    workload = {}
    for row in rows:
        workload[row["guide_id"]] = (row["tours"], row["on_day"] > 0)
    return workload


def find_free_guide(tour_date, language):
    """Pick a guide who speaks the language and is free on that date.

    Fair rotation: the guide with the FEWEST tours that month wins.
    If two guides are tied, the one with the lower ID wins
    (guides are checked in ID order and we only replace on a smaller count).
    Returns None if nobody is free.
    """
    workload = get_guide_workload(tour_date)
    best_guide = None
    best_count = 0

    for guide in get_all_guides():
        if not guide.speaks(language):
            continue
        tours, busy = workload.get(guide.guide_id, (0, False))
        if busy:
            continue
        if best_guide is None or tours < best_count:
            best_guide = guide
            best_count = tours

    return best_guide


# ---------- CRUD ----------

def create_booking(tourist_name, group_size, experience, tour_date, language, user_id):
    """Book a tour. Returns the new Booking, or None if no guide is free.

    The INSERT only happens if the guide still has no confirmed booking that
    day (checked inside the same SQL statement), so two coordinators booking
    at the same moment can never double-book a guide. If we lose that race,
    we simply look for the next free guide.
    """
    total_price = experience.price_for(group_size)
    community_share = calculate_community_share(total_price)

    # At most one attempt per guide, so the loop always ends
    for _ in range(len(get_all_guides()) + 1):
        guide = find_free_guide(tour_date, language)
        if guide is None:
            return None

        # A fresh connection gives lastrowid 0 when the WHERE NOT EXISTS blocked the insert
        new_id = insert(
            "INSERT INTO bookings (tourist_name, group_size, tour_date, language, experience_id, "
            "guide_id, total_price, community_share, status, created_by) "
            "SELECT ?, ?, ?, ?, ?, ?, ?, ?, 'confirmed', ? "
            "WHERE NOT EXISTS (SELECT 1 FROM bookings WHERE guide_id = ? "
            "AND tour_date = ? AND status = 'confirmed')",
            (tourist_name, group_size, tour_date, language, experience.experience_id,
             guide.guide_id, total_price, community_share, user_id,
             guide.guide_id, tour_date),
        )
        if new_id:
            return get_booking_by_id(new_id)
    return None


def get_booking_by_id(booking_id):
    row = fetch_one(BOOKING_SELECT + " WHERE b.booking_id = ?", (booking_id,))
    if row is None:
        return None
    return row_to_booking(row)


def get_bookings_by_date(tour_date):
    rows = fetch_all(BOOKING_SELECT + " WHERE b.tour_date = ? ORDER BY b.booking_id", (tour_date,))
    return rows_to_bookings(rows)


def get_all_bookings():
    rows = fetch_all(BOOKING_SELECT + " ORDER BY b.tour_date, b.booking_id")
    return rows_to_bookings(rows)


def update_booking(booking, new_tourist_name, new_group_size):
    """Change the tourist name and group size, and recalculate the price.

    Only confirmed bookings can be changed. Returns 0 if nothing was updated.
    """
    experience = get_experience_by_id(booking.experience_id)
    if experience is None:
        return 0
    total_price = experience.price_for(new_group_size)
    community_share = calculate_community_share(total_price)
    return execute(
        "UPDATE bookings SET tourist_name = ?, group_size = ?, total_price = ?, community_share = ? "
        "WHERE booking_id = ? AND status = 'confirmed'",
        (new_tourist_name, new_group_size, total_price, community_share, booking.booking_id),
    )


def cancel_booking(booking_id):
    """Mark a confirmed booking as cancelled. Returns 0 if it was not confirmed."""
    return execute(
        "UPDATE bookings SET status = 'cancelled' WHERE booking_id = ? AND status = 'confirmed'",
        (booking_id,),
    )


def delete_booking(booking_id):
    """Remove a booking completely (admin only)."""
    return execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
