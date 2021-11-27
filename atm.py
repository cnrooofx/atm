"""An ATM for users to perform transactions with a bank."""

from bank import Bank
from account import Account
from exceptions import AtmError, AccountError


class ATM:
    """An Automated Teller Machine for user transactions with a bank."""

    def __init__(self, bank: Bank, balance: float = 1000.0):
        """Create a new ATM.

        Args:
            bank (Bank): The bank that this ATM is connected to.
            balance (float, optional): The initial balance. Defaults to 1000.0.
        """
        self._bank = bank
        self._balance = balance
        self._connected_banks = {}

    def __str__(self) -> str:
        """Return a string of the bank which the ATM is connected to."""
        return f"ATM for {self._bank.name}"

    def login(self, iban: int, pin: int) -> Account:
        """Checks with the bank if the user is permitted to login.

        Args:
            iban (int): The bank account identifier of the user.
            pin (int): The user's PIN.

        Raises:
            BankError: If the IBAN or PIN are incorrect.

        Returns:
            Account: The account of the user logging in.
        """
        return self._bank.login(iban, pin)

    def user_check_balance(self, account: Account) -> float:
        """Get the current account balance of a user.

        Args:
            account (Account): The account to get the balance of.

        Returns:
            float: The user's current balance.
        """
        return self._bank.check_balance(account)

    def user_withdraw(self, account: Account, amount: float):
        """Withdraw the given amount from the user's account.

        Args:
            account (Account): The account to withdraw from.
            amount (float): The amount of money to withdraw.

        Raises:
            TypeError: If the account isn't an Account object.
            TypeError: If the amount isn't a float or an int.
            ValueError: If the amount of money is less than or equal to 0.
            AtmError: If the ATM doesn't have enough money for the transaction.
            AccountError: If the given account has been tampered with.
        """
        if not isinstance(account, Account):
            raise TypeError("Not a valid user")
        if not isinstance(amount, (int, float)):
            raise TypeError("Must be of type int or float")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if amount > self._balance:
            raise AtmError("ATM does not have enough funds")
        try:
            self._bank.withdraw(account, amount)
            self._balance -= amount
        except AccountError as error:
            raise AccountError() from error

    def user_deposit(self, account: Account, amount: float):
        """Deposit the given amount into the user's account.

        Args:
            account (Account): THe account to deposit into.
            amount (float): The amount to deposit.

        Raises:
            TypeError: If the account isn't an Account object.
            TypeError: If the amount isn't a float or an int
            ValueError: If the amount is not greater than 0.
        """
        if not isinstance(account, Account):
            raise TypeError("Not a valid user")
        if not isinstance(amount, (int, float)):
            raise TypeError("Must be of type int or float")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self._bank.deposit(account, amount)
        self._balance += amount

    def user_transfer(self, account: Account, amount: float,
                      transfer_bank: str, transfer_iban: int):
        self.user_withdraw(account, amount)
        other_bank = self.get_connected_bank(transfer_bank)
        other_bank.transfer(transfer_iban, amount)

    def user_reset_pin(self, account: Account, new_pin: int):
        if not isinstance(account, Account):
            raise TypeError("Not a valid user")
        self._bank.reset_pin(account, new_pin)

    def admin_withdraw(self, account: Account, amount: float):
        """Remove funds from the ATM, if the user is an admin.

        Args:
            account (Account): The user account (must be an admin).
            amount (float): The amount of money to remove.

        Raises:
            TypeError: If the account is not an Account object.
            TypeError: If the amount is not a float or an int.
            ValueError: If the amount is not greater than 0.
            AccountError: If the user account is not an Admin
            AtmError: If the ATM doesn't have enough money to remove.
        """
        if not isinstance(account, Account):
            raise TypeError("Not a valid user")
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be of type float or int")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not self._bank.check_admin(account):
            raise AccountError("User must be an admin")
        if amount > self._balance:
            raise AtmError("ATM does not have enough funds")
        self._balance -= amount

    def admin_deposit(self, account: Account, amount: float):
        """Add funds to the ATM, if the user is an admin.

        Args:
            account (Account): The user account (must be an admin).
            amount (float): The amount to add to the ATM.

        Raises:
            TypeError: If the account is not an Account object
            TypeError: If the amount is not a float or an int.
            ValueError: If the amount is not greater than 0.
            AccountError: If the user account is not an admin.
        """
        if not isinstance(account, Account):
            raise TypeError("Not a valid user")
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be of type float or int")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not self._bank.check_admin(account):
            raise AccountError("User must be an admin")
        self._balance += amount

    def check_balance(self, account: Account) -> float:
        """Get the total balance of the ATM, if the user is an admin.

        Args:
            account (Account): The user account (must be an admin).

        Raises:
            TypeError: If the account is not an Account object.
            AccountError: If the user account is not an admin.

        Returns:
            float: The total balance of the ATM.
        """
        if not isinstance(account, Account):
            raise TypeError("Not a valid user")
        if not self._bank.check_admin(account):
            raise AccountError("User must be an admin")
        return self._balance

    def add_connected_bank(self, bank: Bank) -> bool:
        """Add a bank connection to this ATM.

        Allows ATM users to transfer funds to other users the added bank.

        Args:
            bank (Bank): The new bank to be added.

        Raises:
            TypeError: If the bank isn't from the Bank class.

        Returns:
            bool: True if the bank was added, otherwise False.
        """
        added = False
        if not isinstance(bank, Bank):
            raise TypeError("Not a valid bank")
        if bank is not self._bank:
            bank_name = bank.name
            if bank_name not in self._connected_banks:
                self._connected_banks[bank_name] = bank
                added = True
        return added

    def is_bank_connected(self, bank_name: str) -> bool:
        """Returns whether the bank is connected to this ATM or not.

        Args:
            bank_name (str): The name of the bank to check for.

        Returns:
            bool: True if the bank is connected, otherwise false.
        """
        connected = False
        if bank_name in self._connected_banks:
            connected = True
        return connected

    def get_connected_bank(self, bank_name: str) -> Bank:
        """Returns the bank object for the specified bank.

        Args:
            bank_name (str): The name of the bank to get.

        Returns:
            Bank: The specified bank, or None if the bank isn't connected.
        """
        if bank_name in self._connected_banks:
            return self._connected_banks[bank_name]

    def get_connected_banks(self) -> dict:
        """Get the dictionary of Banks connected to this ATM.

        Returns:
            dict: The connected banks.
        """
        return self._connected_banks
