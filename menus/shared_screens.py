"""
Screens that BOTH the admin and the coordinator can use.
"""

from services.guide_service import get_all_guides
from services.experience_service import get_all_experiences
from services.booking_service import get_bookings_by_date
from services.report_service import guide_earnings_for_month, community_fund_for_month
from utils.validation import ask_date, ask_month
from utils.display import (print_section, print_guides, print_experiences,
                           print_bookings, format_rwf, pause)


def view_guides_screen():
    print_section("ALL GUIDES")
    print_guides(get_all_guides())
    pause()


def view_experiences_screen():
    print_section("ALL TOUR EXPERIENCES")
    print_experiences(get_all_experiences())
    pause()


def bookings_by_date_screen():
    print_section("BOOKINGS FOR A DATE")
    tour_date = ask_date("Date", allow_past=True)
    print()
    print_bookings(get_bookings_by_date(tour_date))
    pause()


def report_screen():
    print_section("GUIDE EARNINGS & COMMUNITY FUND REPORT")
    month = ask_month("Month")
    rows = guide_earnings_for_month(month)

    print()
    if len(rows) == 0:
        print("No confirmed tours in", month)
    else:
        print("{:<5} {:<24} {:>6} {:>16}".format("Rank", "Guide", "Tours", "Earned"))
        print("-" * 54)
        rank = 1
        for row in rows:
            print("{:<5} {:<24} {:>6} {:>16}".format(
                rank, row["full_name"], row["tours"], format_rwf(row["earnings"])))
            rank = rank + 1

    print()
    print("Community fund total for", month + ":", format_rwf(community_fund_for_month(month)))
    pause()