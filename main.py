"""Install requirements with `pip3 install -r requirements.txt`"""

from rich.console import Console
from rich.panel import Panel

from atm import ATM

console = Console()
atm = ATM()


def start_atm():
    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Welcome"))
        console.print("1) Customer")
        console.print("2) Admin")
        console.print("\nPlease select an option.")

        menu_selection = get_user_selection(["1", "2"])
            
    if menu_selection == "2":
        admin_menu()
    else:
        # Maybe a user login before going to the menu?
        main_menu()


def admin_menu():
    console.clear()
    console.print(Panel.fit("Admin Menu"))


def main_menu():
    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Main Menu"))
        console.print("1) Check Balance")
        console.print("2) Withdraw")
        console.print("3) Deposit")
        console.print("4) Transfer Funds")
        console.print("5) Reset PIN")
        console.print("\nPlease select an option or press (l) to Logout.")

        menu_selection = get_user_selection(["1", "2", "3", "4", "5", "l"])

    if menu_selection == "1":
        print("Check balance")
    elif menu_selection == "2":
        print("Withdraw")
    elif menu_selection == "3":
        print("Deposit")
    elif menu_selection == "4":
        print("Transfer")
    elif menu_selection == "5":
        print("Reset PIN")


def get_user_selection(options):
    """Get user input and check against a list of valid options.

    Args:
        options (list): List of valid input options.

    Returns:
        user_input (str): One of the valid options from the user or None.
    """
    user_input = input("-> ")
    if user_input not in options:
        user_input = None
    return user_input


if __name__ == "__main__":
    # while True:
    start_atm()
