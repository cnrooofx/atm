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

    user1_name = "Aidan"
    user1_pin = 1234

    user2_name = "Dan"
    user2_pin = 2345

    user3_name = "Conor"
    user3_pin = 3456

    user4_name = "Alex"
    user4_pin = 4567

    admin_name = "Admin"
    admin_pin = 0000

    user1 = aib.create_account(user1_name, user1_pin)
    user2 = aib.create_account(user2_name, user2_pin)
    user3 = aib.create_account(user3_name, user3_pin)
    user4 = aib.create_account(user4_name, user4_pin)
    admin = aib.create_admin_account(admin_name, admin_pin)

    boi = Bank("boi", "Bank of Ireland")
    revolut = Bank("revolut", "Revolut")

    transfer_user_name = "Transfer - Mary"
    transfer_user_pin = 1123
    transfer_user = boi.create_account(transfer_user_name, transfer_user_pin)

    aib_atm = ATM(aib)
    # boi_atm = ATM(boi)
    aib_atm.add_connected_bank(boi)
    aib_atm.add_connected_bank(revolut)

    iban_list = []
    iban_list.append((user1, user1_name, user1_pin))
    iban_list.append((user2, user2_name, user2_pin))
    iban_list.append((user3, user3_name, user3_pin))
    iban_list.append((user4, user4_name, user4_pin))
    iban_list.append((admin, admin_name, admin_pin))
    iban_list.append((transfer_user, transfer_user_name, transfer_user_pin))
    return aib_atm, iban_list


def atm_login(atm: ATM):
    console.clear()
    console.print(Panel.fit("Welcome"))
    console.print("Please enter your IBAN")
    iban = input("-> ")
    pin = None
    while pin is None:
        console.clear()
        console.print("Please enter your PIN to login")
        pin = get_user_pin()
    try:
        user = atm.login(iban, pin)
    except exceptions.BankError:
        menu_selection = None
        while menu_selection is None:
            console.clear()
            console.print(Panel.fit("Sorry!"))
            console.print("Invalid IBAN or PIN.")
            console.print("\nPress (q) to quit.")
            menu_selection = get_user_selection(["q"])
        return

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
        user_transfer(atm, user)

    elif menu_selection == "5":
        user_reset_pin(atm, user)


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
    while amount <= 0:
        console.clear()
        console.print(Panel.fit("Withdrawal"))
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
            menu_selection = None
            while menu_selection is None:
                console.clear()
                console.clear()
                console.print(Panel.fit("Sorry!"))
                console.print("Insufficient funds in ATM")
                console.print("Please come back again later")
                console.print("\nPress (q) to quit.")
                menu_selection = get_user_selection(["q"])
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


def user_transfer(atm, user):
    banks = atm.get_connected_banks()
    bank_list = []
    for bank_name in banks:
        bank_list.append(bank_name)

    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Bank Transfer"))
        menu_option = 1
        for bank_name in banks:
            console.print(f"{menu_option}) {bank_name}")
            menu_option += 1
        console.print("\nPress (q) to quit.")
        options = [str(option) for option in range(1, menu_option)] + ["q"]
        menu_selection = get_user_selection(options)
        if menu_selection == "q":
            return

    transfer_bank_name = bank_list[int(menu_selection) - 1]
    transfer_bank = atm.get_connected_bank(transfer_bank_name)

    transferred = False
    error_msg = ""
    while not transferred:
        iban = None
        while iban is None:
            console.clear()
            console.print(Panel.fit(f"Transfer to {transfer_bank_name}"))
            if error_msg:
                console.print(error_msg)
                error_msg = ""
            console.print("Please enter the IBAN of the user to transfer to")
            console.print("or press (q) to quit.")
            iban = get_iban()
            if iban == "q":
                return

        amount = 0.0
        while amount <= 0:
            console.clear()
            console.print(Panel.fit(f"Transfer to Account: {iban}"))
            console.print("Enter the amount to transfer")
            amount = get_amount()
        try:
            atm.user_withdraw(user, amount)
        except exceptions.AccountError:
            error_msg = "Insufficient balance for transfer.\n"
            continue
        try:
            transfer_bank.transfer(iban, amount)
        except exceptions.BankError:
            error_msg = "Invalid IBAN.\n"
            continue
        transferred = True

    menu_selection = None
    while menu_selection is None:
        console.clear()
        console.print(Panel.fit("Thank you"))
        console.print(f"Transferred €{amount} successfully to account {iban}")
        console.print("\nPress (q) to quit.")
        menu_selection = get_user_selection(["q"])


def user_reset_pin(atm, user):
    valid_pin = None
    error_msg = ""
    while valid_pin is None:
        pin = None
        while pin is None:
            console.clear()
            console.print(Panel.fit("Reset PIN"))
            if error_msg:
                console.print(error_msg + "\n")
                error_msg = ""
            console.print("Please enter your new PIN.")
            pin = get_user_pin()
        verify_pin = None
        while verify_pin is None:
            console.clear()
            console.print(Panel.fit("Reset PIN"))
            console.print("Please re-enter the PIN.")
            verify_pin = get_user_pin()
        if pin == verify_pin:
            valid_pin = pin
        else:
            error_msg = "Both PINs must match, please try again."
    atm.user_reset_pin(user, valid_pin)


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


def get_user_pin() -> int:
    user_input = input("-> ")
    if len(user_input) != 4:
        pin = None
    try:
        pin = int(user_input)
    except ValueError:
        pin = None
    return pin


def get_iban() -> int:
    iban = input("-> ")
    if len(iban) != 8:
        iban = None
    else:
        try:
            iban = int(iban)
        except ValueError:
            iban = None
    return iban


if __name__ == "__main__":
    aib_atm, iban_list = setup()

    print(iban_list)
    with open("iban_list.txt", "w", encoding="utf-8") as file:
        for user in iban_list:
            file.write(str(user))
    sleep(5)  # Show the IBANs for 5 seconds before the screen gets cleared

    while True:
        atm_login(aib_atm)
