"""
Menu for the COORDINATOR role: books tours and manages bookings.
The coordinator can only VIEW guides and experiences, not change them.
"""

from services.experience_service import get_all_experiences, get_experience_by_id
from services.booking_service import (create_booking, get_booking_by_id,
                                      update_booking, cancel_booking)
from menus.shared_screens import (view_guides_screen, view_experiences_screen,
                                  bookings_by_date_screen, report_screen)
from utils.validation import (LANGUAGES, LANGUAGE_NAMES, ask_text, ask_int,
                              ask_date, ask_choice, ask_yes_no)
from utils.display import (print_header, print_section, print_experiences,
                           print_booking_details, pause)

MAX_GROUP_SIZE = 20


def book_tour_screen(user):
    print_section("[3] BOOK A TOUR FOR A TOURIST")
    experiences = get_all_experiences()
    if len(experiences) == 0:
        print("There are no experiences yet. Ask the admin to add one.")
        pause()
        return

    tourist_name = ask_text("Tourist name")
    group_size = ask_int("Number of people", 1, MAX_GROUP_SIZE)

    print()
    print_experiences(experiences)
    experience = None
    while experience is None:
        experience_id = ask_int("Experience ID", 1, 999999)
        experience = get_experience_by_id(experience_id)
        if experience is None:
            print("  [!] No experience with that ID. Please choose from the list.")

    tour_date = ask_date("Date", allow_past=False)
    language = ask_choice("Preferred language (" + "/".join(LANGUAGES) + ")", LANGUAGES)

    print()
    print("Searching for a free guide who speaks " + LANGUAGE_NAMES[language] + "...")
    booking = create_booking(tourist_name, group_size, experience, tour_date, language, user.user_id)

    if booking is None:
        print("[X] Sorry, no guide who speaks " + LANGUAGE_NAMES[language]
              + " is free on " + tour_date + ". Try another date or language.")
    else:
        print("[OK] Booking " + str(booking.booking_id) + " confirmed!")
        print_booking_details(booking)
    pause()


def ask_booking():
    """Ask for a booking ID and return the Booking, or None if it does not exist."""
    booking_id = ask_int("Booking ID", 1, 999999)
    booking = get_booking_by_id(booking_id)
    if booking is None:
        print("[X] No booking with ID", booking_id)
    return booking


def update_booking_screen():
    print_section("UPDATE A BOOKING")
    booking = ask_booking()
    if booking is None:
        pause()
        return
    if booking.status != "confirmed":
        print("[X] Only confirmed bookings can be updated.")
        pause()
        return

    print_booking_details(booking)
    print("\nPress Enter to keep the value in [brackets].")
    new_name = ask_text("Tourist name", booking.tourist_name)
    new_size = ask_int("Number of people", 1, MAX_GROUP_SIZE, booking.group_size)

    update_booking(booking, new_name, new_size)
    print("[OK] Booking", booking.booking_id, "updated.")
    print_booking_details(get_booking_by_id(booking.booking_id))
    pause()


def cancel_booking_screen():
    print_section("CANCEL A BOOKING")
    booking = ask_booking()
    if booking is None:
        pause()
        return

    print_booking_details(booking)
    if booking.status != "confirmed":
        print("[X] This booking is already cancelled.")
    elif ask_yes_no("Cancel this booking?"):
        cancel_booking(booking.booking_id)
        print("[OK] Booking", booking.booking_id, "cancelled. The guide is free again that day.")
    else:
        print("Nothing changed.")
    pause()


def coordinator_menu(user):
    while True:
        print_header("COORDINATOR MENU  (logged in as " + user.full_name + ")")
        print(" 1. View guides")
        print(" 2. View tour experiences")
        print(" 3. Book a tour for a tourist")
        print(" 4. View bookings for a date")
        print(" 5. Update a booking")
        print(" 6. Cancel a booking")
        print(" 7. Guide earnings & community fund report")
        print(" 0. Log out")
        choice = input("\nType a number (0-7) and press Enter: ").strip()

        if choice == "1":
            view_guides_screen()
        elif choice == "2":
            view_experiences_screen()
        elif choice == "3":
            book_tour_screen(user)
        elif choice == "4":
            bookings_by_date_screen()
        elif choice == "5":
            update_booking_screen()
        elif choice == "6":
            cancel_booking_screen()
        elif choice == "7":
            report_screen()
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("  [!] Invalid choice. Please type a number from 0 to 7.")