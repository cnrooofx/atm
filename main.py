"""The user interface of the ATM.

Install requirements with `pip3 install -r requirements.txt`
"""

from time import sleep
from rich.console import Console
from rich.panel import Panel

from atm import ATM
from bank import Bank
import exceptions

console = Console()


def setup():
    aib = Bank("aib", "Allied Irish Banks")

    user1 = aib.create_account("Aidan", 1234)
    user2 = aib.create_account("Dan", 2345)
    user3 = aib.create_account("Conor", 3456)
    user4 = aib.create_account("Alex", 4567)
    admin = aib.create_admin_account("Conor", 1010)

    boi = Bank("boi", "Bank of Ireland")
    boi.create_account("Mary", 1123)

    aib_atm = ATM(aib)
    # boi_atm = ATM(boi)
    aib_atm.add_connected_bank(boi)

    iban_list = [user1, user2, user3, user4, admin]
    return aib_atm, iban_list


def atm_login(atm: ATM):
    console.clear()
    console.print(Panel.fit("Welcome"))
    console.print("Please enter your IBAN to login")
    iban = input("-> ")
    user = atm.login(iban)

    if user.admin:
        admin_menu(atm, user)
    else:
        main_menu(atm, user)


def main_menu(atm, user):
    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(f"Welcome {user.name}")
        console.print(Panel.fit("Main Menu"))
        console.print("1) Check Balance")
        console.print("2) Withdraw")
        console.print("3) Deposit")
        console.print("4) Transfer Funds")
        console.print("5) Reset PIN")
        console.print("\nPlease select an option or press (q) to quit.")

        menu_selection = get_user_selection(["1", "2", "3", "4", "5", "q"])

    if menu_selection == "1":
        user_check_balance(atm, user)

    elif menu_selection == "2":
        user_withdraw(atm, user)

    elif menu_selection == "3":
        user_deposit(atm, user)

    elif menu_selection == "4":
        print("Transfer")

    elif menu_selection == "5":
        print("Reset PIN")


def user_check_balance(atm, user):
    balance = atm.user_check_balance(user)
    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Balance"))
        console.print(f"You have €{balance} in your account.")
        console.print("\nPress (q) to quit.")
        menu_selection = get_user_selection(["q"])


def user_withdraw(atm, user):
    amount = 0.0
    error_msg = ""
    while amount <= 0:
        console.clear()
        console.print(Panel.fit("Withdrawal"))
        if error_msg:
            console.print(error_msg)
        console.print("Enter the amount to withdraw")
        amount = get_amount()
        try:
            atm.user_withdraw(user, amount)
        except exceptions.AccountError:
            menu_selection = None
            while menu_selection is None:
                console.clear()
                console.print(Panel.fit("Sorry!"))
                console.print("Insufficient funds in your account")
                console.print("\nPress (q) to quit.")
                menu_selection = get_user_selection(["q"])
            return

        except exceptions.AtmError:
            console.clear()
            console.print(Panel.fit("Sorry!"))
            console.print("Insufficient funds in ATM")
            console.print(" Please come back again later")
            return

    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Thank you"))
        console.print(f"€{amount} removed from your account")
        console.print("\nPress (q) to quit.")
        menu_selection = get_user_selection(["q"])


def user_deposit(atm, user):
    amount = 0.0
    while amount <= 0:
        console.clear()
        console.print(Panel.fit("Deposit"))
        console.print("Enter the amount to deposit")
        amount = get_amount()
        try:
            atm.user_deposit(user, amount)
        except exceptions.AccountError:
            pass
        except exceptions.AtmError:
            console.clear()
            console.print(Panel.fit("Sorry!"))
            console.print("Insufficient funds in ATM")
            console.print(" Please come back again later")
            return

    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Thank you"))
        console.print(f"Deposited €{amount} into your account")
        console.print("\nPress (q) to quit.")
        menu_selection = get_user_selection(["q"])


def admin_menu(atm, user):
    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(f"Welcome {user.name}")
        console.print(Panel.fit("Admin Menu"))
        console.print("1) Check ATM Balance")
        console.print("2) Top up Money")
        console.print("3) Remove Money")
        console.print("\nPlease select an option or press (q) to quit.")

        menu_selection = get_user_selection(["1", "2", "3", "q"])

    if menu_selection == "1":
        admin_check_balance(atm, user)

    elif menu_selection == "2":
        admin_top_up(atm, user)

    elif menu_selection == "3":
        admin_withdraw(atm, user)


def admin_check_balance(atm, user):
    balance = atm.check_balance(user)
    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Total ATM Balance"))
        console.print(f"€{balance}")
        console.print("\nPress (q) to quit.")
        menu_selection = get_user_selection(["q"])


def admin_top_up(atm, user):
    amount = 0
    while amount <= 0:
        console.clear()
        console.print(Panel.fit("Top-up ATM Balance"))
        console.print("Enter the amount to top up by")
        amount = get_amount()

    atm.admin_deposit(user, amount)

    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Thank you"))
        console.print(f"ATM Balance topped up by €{amount}")
        console.print("\nPress (q) to quit.")
        menu_selection = get_user_selection(["q"])


def admin_withdraw(atm, user):
    amount = 0.0
    error_msg = ""
    while amount <= 0:
        console.clear()
        console.print(Panel.fit("Remove Money"))
        if error_msg:
            console.print(error_msg)
        console.print("Enter the amount to remove")
        amount = get_amount()
        try:
            atm.admin_withdraw(user, amount)
        except exceptions.AtmError:
            error_msg = "Insufficient funds in ATM"
            amount = 0.0

    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Thank you"))
        console.print(f"€{amount} removed from ATM")
        console.print("\nPress (q) to quit.")
        menu_selection = get_user_selection(["q"])


def get_user_selection(options: list) -> str:
    """Get user input and check against a list of valid options.

    Args:
        options (list): List of valid input options as strings.

    Returns:
        user_input (str): One of the valid options from the user or None.
    """
    user_input = input("-> ")
    if user_input not in options:
        user_input = None
    return user_input


def get_amount() -> float:
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

    aib_atm, iban_list = setup()

    print(iban_list)
    sleep(5)  # Show the IBANs for 5 seconds before the screen gets cleared

    while True:
        atm_login(aib_atm)
