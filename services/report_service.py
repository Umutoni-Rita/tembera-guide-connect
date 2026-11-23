"""
Monthly earnings and community fund report.
"""

from database.connection import fetch_all, fetch_one


def guide_earnings_for_month(month):
    """Each guide's tours and earnings for a month like '2026-11'.

    Only confirmed bookings count. Highest earner first.
    A guide earns the total price minus the community share.
    """
    return fetch_all(
        """
        SELECT g.guide_id, g.full_name,
               COUNT(b.booking_id) AS tours,
               SUM(b.total_price - b.community_share) AS earnings
        FROM bookings b
        JOIN guides g ON b.guide_id = g.guide_id
        WHERE b.status = 'confirmed' AND b.tour_date LIKE ?
        GROUP BY g.guide_id
        ORDER BY earnings DESC
        """,
        (month + "%",),
    )


def community_fund_for_month(month):
    """Total money going to the community fund in that month."""
    row = fetch_one(
        "SELECT SUM(community_share) AS fund FROM bookings "
        "WHERE status = 'confirmed' AND tour_date LIKE ?",
        (month + "%",),
    )
    if row["fund"] is None:
        return 0
    return row["fund"]
