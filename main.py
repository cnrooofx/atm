"""Install requirements with `pip3 install -r requirements.txt`"""

from rich.console import Console
from rich.panel import Panel

from atm import ATM
from account import Account
from bank import Bank


console = Console()
aib = Bank("aib")
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
        admin = Account(1, 2345, "admin@aib.ie", aib, True)
        admin_menu(admin)
    else:
        user = Account(123, 9876, "user1@aib.ie", aib, False)
        main_menu(user)


def admin_menu(user):
    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Admin Menu"))
        console.print("1) Check ATM Balance")
        console.print("2) Top up Money")
        console.print("3) Remove Money")
        console.print("\nPlease select an option or press (q) to quit.")

        menu_selection = get_user_selection(["1", "2", "3", "q"])

    if menu_selection == "1":
        balance = atm.check_balance(user)
        menu_selection = None
        while menu_selection is None:
            console.clear()
            console.print(Panel.fit("Total ATM Balance"))
            console.print(f"€{balance}")
            console.print("\nPress (q) to quit.")
            menu_selection = get_user_selection(["q"])

    elif menu_selection == "2":
        amount = 0
        while amount <= 0:
            console.clear()
            console.print(Panel.fit("Top-up ATM Balance"))
            console.print("Enter the amount to top up by")
            amount = get_float_amount()

        atm.admin_deposit(user, amount)

        menu_selection = None
        while menu_selection is None:
            console.clear()
            console.print(Panel.fit("Thank you"))
            console.print(f"ATM Balance topped up by €{amount}")
            console.print("\nPress (q) to quit.")
            menu_selection = get_user_selection(["q"])

    elif menu_selection == "3":
        amount = 0
        error_msg = ""
        while amount <= 0:
            console.clear()
            console.print(Panel.fit("Remove Money"))
            if error_msg:
                console.print(error_msg)
            console.print("Enter the amount to remove")
            amount = get_float_amount()
            try:
                atm.admin_withdraw(user, amount)
            except ValueError:
                error_msg = "Insufficient funds in ATM"
                amount = 0.0

        menu_selection = None
        while menu_selection is None:
            console.clear()
            console.print(Panel.fit("Thank you"))
            console.print(f"€{amount} removed from ATM")
            console.print("\nPress (q) to quit.")
            menu_selection = get_user_selection(["q"])


def main_menu(user):
    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Main Menu"))
        console.print("1) Check Balance")
        console.print("2) Withdraw")
        console.print("3) Deposit")
        console.print("4) Transfer Funds")
        console.print("5) Reset PIN")
        console.print("\nPlease select an option or press (q) to quit.")

        menu_selection = get_user_selection(["1", "2", "3", "4", "5", "q"])

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


def get_float_amount():
    """Get user input as a float.

    Returns:
        (float): The input value as a float, or 0.0 if input was invalid.
    """
    user_input = input("-> ")
    try:
        amount = float(user_input)
    except ValueError:
        amount = 0.0
    return amount

if __name__ == "__main__":
    # while True:
    start_atm()
