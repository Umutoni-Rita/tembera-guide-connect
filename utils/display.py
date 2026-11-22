"""
Printing helpers: headers, money, and tables of guides, experiences and bookings.
"""

from utils.validation import LANGUAGE_NAMES


def print_header(title):
    print()
    print("=" * 60)
    print("  " + title)
    print("=" * 60)


def print_section(title):
    print()
    print("--- " + title + " ---")


def pause():
    input("\nPress Enter to continue...")


def format_rwf(amount):
    """30000 -> '30,000 RWF'"""
    return "{:,} RWF".format(int(amount))


def language_names(codes):
    """["EN", "FR"] -> 'English, French'"""
    names = []
    for code in codes:
        names.append(LANGUAGE_NAMES[code])
    return ", ".join(names)


def print_guides(guides):
    if len(guides) == 0:
        print("No guides registered yet.")
        return
    print("{:<4} {:<22} {:<12} {:<4} {}".format("ID", "Name", "Phone", "Sex", "Languages"))
    print("-" * 70)
    for guide in guides:
        print("{:<4} {:<22} {:<12} {:<4} {}".format(
            guide.guide_id, guide.full_name, guide.phone, guide.gender,
            language_names(guide.languages)))


def print_experiences(experiences):
    if len(experiences) == 0:
        print("No experiences added yet.")
        return
    print("{:<4} {:<36} {:<18} {:>14} {:>6}".format("ID", "Experience", "Location", "Price/person", "Hours"))
    print("-" * 82)
    for experience in experiences:
        print("{:<4} {:<36} {:<18} {:>14} {:>6g}".format(
            experience.experience_id, experience.name, experience.location,
            format_rwf(experience.price_per_person), experience.duration_hours))


def print_bookings(bookings):
    if len(bookings) == 0:
        print("No bookings found.")
        return
    print("{:<4} {:<11} {:<16} {:>3} {:<30} {:<18} {:>12} {:<10}".format(
        "ID", "Date", "Tourist", "Ppl", "Experience", "Guide", "Total", "Status"))
    print("-" * 112)
    for booking in bookings:
        print("{:<4} {:<11} {:<16} {:>3} {:<30} {:<18} {:>12} {:<10}".format(
            booking.booking_id, booking.tour_date, booking.tourist_name[:16],
            booking.group_size, booking.experience_name[:30], booking.guide_name[:18],
            format_rwf(booking.total_price), booking.status))


def print_booking_details(booking):
    print("     Booking ID : " + str(booking.booking_id))
    print("     Tourist    : " + booking.tourist_name + " (" + str(booking.group_size) + " people)")
    print("     Experience : " + str(booking.experience_id) + " - " + booking.experience_name)
    print("     Guide      : " + booking.guide_name)
    print("     Date       : " + booking.tour_date)
    print("     Language   : " + LANGUAGE_NAMES[booking.language])
    print("     Total      : " + format_rwf(booking.total_price)
          + " (community fund share: " + format_rwf(booking.community_share) + ")")
    print("     Status     : " + booking.status)