import sqlite3
from getpass import getpass

from database.connection import setup_database
from services.auth_service import login
from menus.admin_menu import admin_menu
from menus.coordinator_menu import coordinator_menu
from utils.display import print_header

MAX_LOGIN_ATTEMPTS = 3


def login_screen():
    """Ask for username and password (3 tries) and open the right menu for the role."""
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        username = input("Username: ").strip().lower()
        password = getpass("Password (hidden while typing): ")
        user = login(username, password)

        if user is None:
            attempts = attempts + 1
            print("[X] Wrong username or password.", MAX_LOGIN_ATTEMPTS - attempts, "tries left.")
            continue

        print("[OK] Welcome, " + user.full_name + " (" + user.role + ")")
        # The role decides which menu the user is allowed to see
        if user.is_admin():
            admin_menu(user)
        else:
            coordinator_menu(user)
        return

    print("Too many wrong tries. Returning to the start screen.")


def main():
    if setup_database():
        print("New database created with sample data.")

    while True:
        print_header("WELCOME TO TEMBERA GUIDE CONNECT")
        print("Community tourism bookings - fair tours for every local guide")
        print()
        print(" 1. Log in")
        print(" 0. Exit program")
        choice = input("\nType a number (0-1) and press Enter: ").strip()

        if choice == "1":
            try:
                login_screen()
            except sqlite3.Error as error:
                # Safety net: a database problem shows a message instead of crashing
                print("[X] Database error:", error)
        elif choice == "0":
            print("Goodbye! Murakoze.")
            break
        else:
            print("  [!] Invalid choice. Please type 1 or 0.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or closing the input should exit politely, not show an error
        print("\nGoodbye! Murakoze.")
