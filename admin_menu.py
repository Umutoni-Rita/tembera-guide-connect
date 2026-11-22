"""
Menu for the ADMIN role: manages guides, experiences, bookings and accounts.
"""

import sqlite3

from models.guide import Guide
from models.experience import Experience
from services.guide_service import (add_guide, get_all_guides, get_guide_by_id,
                                    update_guide, delete_guide)
from services.experience_service import (add_experience, get_all_experiences,
                                         get_experience_by_id, update_experience,
                                         delete_experience)
from services.booking_service import get_all_bookings, get_booking_by_id, delete_booking
from menus.shared_screens import (view_guides_screen, view_experiences_screen,
                                  bookings_by_date_screen, report_screen)
from menus.user_accounts_menu import user_accounts_menu
from utils.validation import (LANGUAGES, ask_text, ask_int, ask_positive_number,
                              ask_phone, ask_choice, ask_languages, ask_yes_no)
from utils.display import (print_header, print_section, print_guides, print_experiences,
                           print_bookings, print_booking_details, pause)


# ==================== GUIDES ====================

def register_guide_screen():
    print_section("REGISTER A NEW GUIDE")
    full_name = ask_text("Full name")
    phone = ask_phone("Phone number (10 digits)")
    gender = ask_choice("Gender (F/M)", ["F", "M"])
    languages = ask_languages("Languages spoken, separated by commas (" + "/".join(LANGUAGES) + ")")

    guide = Guide(None, full_name, phone, gender, languages)
    try:
        new_id = add_guide(guide)
        print("[OK] Guide", new_id, "registered:", full_name)
    except sqlite3.IntegrityError:
        print("[X] A guide with phone number", phone, "already exists.")
    pause()


def update_guide_screen():
    print_section("UPDATE A GUIDE")
    print_guides(get_all_guides())
    guide = get_guide_by_id(ask_int("Guide ID to update", 1, 999999))
    if guide is None:
        print("[X] No guide with that ID.")
        pause()
        return

    print("Press Enter to keep the value in [brackets].")
    guide.full_name = ask_text("Full name", guide.full_name)
    guide.phone = ask_phone("Phone number", guide.phone)
    guide.gender = ask_choice("Gender (F/M)", ["F", "M"], guide.gender)
    guide.languages = ask_languages("Languages (" + "/".join(LANGUAGES) + ")", guide.languages)

    try:
        update_guide(guide)
        print("[OK] Guide", guide.guide_id, "updated.")
    except sqlite3.IntegrityError:
        print("[X] Another guide already uses phone number", guide.phone)
    pause()


def delete_guide_screen():
    print_section("DELETE A GUIDE")
    print_guides(get_all_guides())
    guide = get_guide_by_id(ask_int("Guide ID to delete", 1, 999999))
    if guide is None:
        print("[X] No guide with that ID.")
        pause()
        return

    if not ask_yes_no("Delete " + guide.full_name + "?"):
        print("Nothing changed.")
        pause()
        return
    try:
        delete_guide(guide.guide_id)
        print("[OK] Guide", guide.guide_id, "deleted.")
    except sqlite3.IntegrityError:
        # The foreign key in the bookings table protects the booking history
        print("[X] Cannot delete", guide.full_name, "because they have bookings in the system.")
    pause()


def manage_guides_menu():
    while True:
        print_header("MANAGE GUIDES")
        print(" 1. Register a new guide")
        print(" 2. View all guides")
        print(" 3. Update a guide")
        print(" 4. Delete a guide")
        print(" 0. Back")
        choice = input("\nType a number (0-4): ").strip()
        if choice == "1":
            register_guide_screen()
        elif choice == "2":
            view_guides_screen()
        elif choice == "3":
            update_guide_screen()
        elif choice == "4":
            delete_guide_screen()
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice.")


# ==================== EXPERIENCES ====================

def add_experience_screen():
    print_section("ADD A TOUR EXPERIENCE")
    name = ask_text("Experience name")
    location = ask_text("Location")
    price = ask_int("Price per person (RWF)", 1, 10000000)
    hours = ask_positive_number("Duration in hours")

    experience = Experience(None, name, location, price, hours)
    try:
        new_id = add_experience(experience)
        print("[OK] Experience", new_id, "added.\n")
        print_experiences(get_all_experiences())
    except sqlite3.IntegrityError:
        print("[X] An experience called", name, "already exists.")
    pause()


def update_experience_screen():
    print_section("UPDATE A TOUR EXPERIENCE")
    print_experiences(get_all_experiences())
    experience = get_experience_by_id(ask_int("Experience ID to update", 1, 999999))
    if experience is None:
        print("[X] No experience with that ID.")
        pause()
        return

    print("Press Enter to keep the value in [brackets].")
    print("Note: a new price only applies to NEW bookings.")
    experience.name = ask_text("Experience name", experience.name)
    experience.location = ask_text("Location", experience.location)
    experience.price_per_person = ask_int("Price per person (RWF)", 1, 10000000,
                                          experience.price_per_person)
    experience.duration_hours = ask_positive_number("Duration in hours", experience.duration_hours)

    try:
        update_experience(experience)
        print("[OK] Experience", experience.experience_id, "updated.")
    except sqlite3.IntegrityError:
        print("[X] Another experience already has that name.")
    pause()


def delete_experience_screen():
    print_section("DELETE A TOUR EXPERIENCE")
    print_experiences(get_all_experiences())
    experience = get_experience_by_id(ask_int("Experience ID to delete", 1, 999999))
    if experience is None:
        print("[X] No experience with that ID.")
        pause()
        return

    if not ask_yes_no("Delete '" + experience.name + "'?"):
        print("Nothing changed.")
        pause()
        return
    try:
        delete_experience(experience.experience_id)
        print("[OK] Experience", experience.experience_id, "deleted.")
    except sqlite3.IntegrityError:
        print("[X] Cannot delete this experience because it has bookings in the system.")
    pause()


def manage_experiences_menu():
    while True:
        print_header("MANAGE TOUR EXPERIENCES")
        print(" 1. Add a tour experience")
        print(" 2. View all experiences")
        print(" 3. Update an experience")
        print(" 4. Delete an experience")
        print(" 0. Back")
        choice = input("\nType a number (0-4): ").strip()
        if choice == "1":
            add_experience_screen()
        elif choice == "2":
            view_experiences_screen()
        elif choice == "3":
            update_experience_screen()
        elif choice == "4":
            delete_experience_screen()
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice.")


# ==================== BOOKINGS ====================

def view_all_bookings_screen():
    print_section("ALL BOOKINGS")
    print_bookings(get_all_bookings())
    pause()


def delete_booking_screen():
    print_section("DELETE A BOOKING PERMANENTLY")
    booking = get_booking_by_id(ask_int("Booking ID to delete", 1, 999999))
    if booking is None:
        print("[X] No booking with that ID.")
        pause()
        return

    print_booking_details(booking)
    print("Tip: coordinators CANCEL bookings. Delete only removes mistakes or test data.")
    if ask_yes_no("Delete this booking forever?"):
        delete_booking(booking.booking_id)
        print("[OK] Booking", booking.booking_id, "deleted.")
    else:
        print("Nothing changed.")
    pause()


def manage_bookings_menu():
    while True:
        print_header("MANAGE BOOKINGS")
        print(" 1. View all bookings")
        print(" 2. View bookings for a date")
        print(" 3. Delete a booking permanently")
        print(" 0. Back")
        choice = input("\nType a number (0-3): ").strip()
        if choice == "1":
            view_all_bookings_screen()
        elif choice == "2":
            bookings_by_date_screen()
        elif choice == "3":
            delete_booking_screen()
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice.")


# ==================== MAIN ADMIN MENU ====================

def admin_menu(user):
    while True:
        print_header("ADMIN MENU  (logged in as " + user.full_name + ")")
        print(" 1. Manage guides")
        print(" 2. Manage tour experiences")
        print(" 3. Manage bookings")
        print(" 4. Manage user accounts")
        print(" 5. Guide earnings & community fund report")
        print(" 0. Log out")
        choice = input("\nType a number (0-5) and press Enter: ").strip()

        if choice == "1":
            manage_guides_menu()
        elif choice == "2":
            manage_experiences_menu()
        elif choice == "3":
            manage_bookings_menu()
        elif choice == "4":
            user_accounts_menu(user)
        elif choice == "5":
            report_screen()
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("  [!] Invalid choice. Please type a number from 0 to 5.")
