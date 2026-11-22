"""
Admin screens to register (create) and manage login accounts.
"""

import sqlite3
from getpass import getpass

from services.auth_service import (create_user, get_all_users, get_user_by_id,
                                   update_user, reset_password, delete_user)
from utils.validation import ask_text, ask_int, ask_choice, ask_yes_no
from utils.display import print_header, print_section, pause

ROLES = ["ADMIN", "COORDINATOR"]
MIN_PASSWORD_LENGTH = 6


def ask_new_password():
    """Ask for a password twice and make sure both match."""
    while True:
        password = getpass("Password (at least 6 characters, hidden while typing): ")
        if len(password) < MIN_PASSWORD_LENGTH:
            print("  [!] The password is too short.")
            continue
        confirm = getpass("Type the password again: ")
        if password != confirm:
            print("  [!] The passwords do not match. Try again.")
            continue
        return password


def print_users(users):
    print("{:<4} {:<16} {:<24} {}".format("ID", "Username", "Full name", "Role"))
    print("-" * 58)
    for user in users:
        print("{:<4} {:<16} {:<24} {}".format(user.user_id, user.username, user.full_name, user.role))


def create_user_screen():
    print_section("REGISTER A NEW USER ACCOUNT")
    username = ask_text("Username").lower()
    full_name = ask_text("Full name")
    role = ask_choice("Role (ADMIN/COORDINATOR)", ROLES).lower()
    password = ask_new_password()
    try:
        new_id = create_user(username, password, full_name, role)
        print("[OK] Account", new_id, "created for", username, "as", role + ".")
    except sqlite3.IntegrityError:
        print("[X] The username", username, "is already taken.")
    pause()


def view_users_screen():
    print_section("ALL USER ACCOUNTS")
    print_users(get_all_users())
    pause()


def ask_user_account():
    print_users(get_all_users())
    user = get_user_by_id(ask_int("User ID", 1, 999999))
    if user is None:
        print("[X] No user with that ID.")
    return user


def update_user_screen(logged_in_user):
    print_section("UPDATE A USER ACCOUNT")
    user = ask_user_account()
    if user is None:
        pause()
        return
    print("Press Enter to keep the value in [brackets].")
    full_name = ask_text("Full name", user.full_name)
    if user.user_id == logged_in_user.user_id:
        # Stops the admin from removing their own admin rights by mistake
        print("(You cannot change your own role.)")
        role = user.role
    else:
        role = ask_choice("Role (ADMIN/COORDINATOR)", ROLES, user.role.upper()).lower()
    update_user(user.user_id, full_name, role)
    print("[OK] Account", user.user_id, "updated.")
    pause()


def reset_password_screen():
    print_section("RESET A PASSWORD")
    user = ask_user_account()
    if user is None:
        pause()
        return
    reset_password(user.user_id, ask_new_password())
    print("[OK] Password changed for", user.username)
    pause()


def delete_user_screen(logged_in_user):
    print_section("DELETE A USER ACCOUNT")
    user = ask_user_account()
    if user is None:
        pause()
        return
    if user.user_id == logged_in_user.user_id:
        print("[X] You cannot delete your own account while logged in.")
        pause()
        return
    if ask_yes_no("Delete the account '" + user.username + "'?"):
        delete_user(user.user_id)
        print("[OK] Account deleted. Their old bookings are kept.")
    else:
        print("Nothing changed.")
    pause()


def user_accounts_menu(logged_in_user):
    while True:
        print_header("MANAGE USER ACCOUNTS")
        print(" 1. Register a new user account")
        print(" 2. View all accounts")
        print(" 3. Update an account (name / role)")
        print(" 4. Reset a password")
        print(" 5. Delete an account")
        print(" 0. Back")
        choice = input("\nType a number (0-5): ").strip()
        if choice == "1":
            create_user_screen()
        elif choice == "2":
            view_users_screen()
        elif choice == "3":
            update_user_screen(logged_in_user)
        elif choice == "4":
            reset_password_screen()
        elif choice == "5":
            delete_user_screen(logged_in_user)
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice.")