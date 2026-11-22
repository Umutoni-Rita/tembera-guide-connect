"""
Input helpers. Each one keeps asking until the user types something valid,
so the app never crashes on bad input.

Most helpers take an optional `current` value. When updating a record,
the user can press Enter to keep the current value.
"""

from datetime import datetime, date

LANGUAGES = ["EN", "FR", "KIN", "SW"]
LANGUAGE_NAMES = {"EN": "English", "FR": "French", "KIN": "Kinyarwanda", "SW": "Swahili"}


def make_prompt(prompt, current):
    if current is None:
        return prompt + ": "
    return prompt + " [" + str(current) + "]: "


def ask_text(prompt, current=None):
    """Ask for text that is not empty."""
    while True:
        answer = input(make_prompt(prompt, current)).strip()
        if answer == "" and current is not None:
            return current
        if answer != "":
            return answer
        print("  [!] This cannot be empty. Please try again.")


def ask_int(prompt, minimum, maximum, current=None):
    """Ask for a whole number between minimum and maximum."""
    while True:
        answer = input(make_prompt(prompt, current)).strip()
        if answer == "" and current is not None:
            return current
        try:
            number = int(answer)
        except ValueError:
            print("  [!] Please type a whole number, for example 2.")
            continue
        if number < minimum or number > maximum:
            print("  [!] Please type a number from", minimum, "to", str(maximum) + ".")
            continue
        return number


def ask_positive_number(prompt, current=None):
    """Ask for a number bigger than 0 (decimals allowed, like 1.5)."""
    while True:
        answer = input(make_prompt(prompt, current)).strip()
        if answer == "" and current is not None:
            return current
        try:
            number = float(answer)
        except ValueError:
            print("  [!] Please type a number, for example 2 or 1.5.")
            continue
        if number <= 0:
            print("  [!] The number must be bigger than 0.")
            continue
        return number


def ask_phone(prompt, current=None):
    """Ask for a 10-digit phone number like 0781234567."""
    while True:
        answer = input(make_prompt(prompt, current)).strip()
        if answer == "" and current is not None:
            return current
        if len(answer) == 10 and answer.isdigit():
            return answer
        print("  [!] The phone number must have exactly 10 digits, for example 0781234567.")


def ask_choice(prompt, options, current=None):
    """Ask the user to type one of the given options, for example F or M."""
    while True:
        answer = input(make_prompt(prompt, current)).strip().upper()
        if answer == "" and current is not None:
            return current
        if answer in options:
            return answer
        print("  [!] Please type one of:", "/".join(options))


def ask_languages(prompt, current=None):
    """Ask for one or more language codes separated by commas, e.g. EN,FR.

    Returns a list like ["EN", "FR"].
    """
    current_text = None
    if current is not None:
        current_text = ",".join(current)

    while True:
        answer = input(make_prompt(prompt, current_text)).strip().upper()
        if answer == "" and current is not None:
            return current

        languages = []
        all_valid = True
        for part in answer.split(","):
            code = part.strip()
            if code == "":
                continue
            if code not in LANGUAGES:
                print("  [!]", code, "is not a known language. Use:", "/".join(LANGUAGES))
                all_valid = False
                break
            if code not in languages:
                languages.append(code)

        if all_valid and len(languages) > 0:
            return languages
        if all_valid:
            print("  [!] Please give at least one language.")


def ask_date(prompt, allow_past):
    """Ask for a date in the format YYYY-MM-DD. Returns it as text."""
    while True:
        answer = input(prompt + " (YYYY-MM-DD): ").strip()
        try:
            chosen_date = datetime.strptime(answer, "%Y-%m-%d").date()
        except ValueError:
            print("  [!] Please use the format YYYY-MM-DD, for example 2026-12-05.")
            continue
        if not allow_past and chosen_date < date.today():
            print("  [!] The date cannot be in the past.")
            continue
        return answer


def ask_month(prompt):
    """Ask for a month in the format YYYY-MM. Returns it as text."""
    while True:
        answer = input(prompt + " (YYYY-MM): ").strip()
        try:
            datetime.strptime(answer, "%Y-%m")
        except ValueError:
            print("  [!] Please use the format YYYY-MM, for example 2026-11.")
            continue
        return answer


def ask_yes_no(prompt):
    """Return True for yes and False for no."""
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer == "y" or answer == "yes":
            return True
        if answer == "n" or answer == "no":
            return False
        print("  [!] Please type y or n.")