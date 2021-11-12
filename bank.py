"""A bank to be used with an ATM."""

import shelve

from account import Account
from exceptions import BankError, AccountError


class Bank:
    """A bank that contains a database of accounts."""

    def __init__(self, bank_id: str, bank_name: str):
        """Create a new Bank.

        Args:
            bank_id (str): Short identifier for the bank (Must have no spaces).
            bank_name (str): Longer name of the bank for printing strings.
        """
        self._name = bank_name
        self._database = f"{bank_id}_bank_accounts"
        self._next_iban = 1

    def __str__(self) -> str:
        """Returns a string of the name of the Bank."""
        return str(self._name)

    def __contains__(self, iban: int) -> bool:
        """Returns whether or not the account is in this bank.

        Args:
            iban (int): The IBAN of the account to check.

        Returns:
            bool: True if the account is in the bank, otherwise False.
        """
        contained = False
        with shelve.open(self._database) as accounts:
            if str(iban) in accounts:
                contained = True
        return contained

    @property
    def name(self):
        """Get the name of the Bank."""
        return self._name

    def get_account(self, iban: int) -> Account:
        """Get the user account corresponding to the given IBAN.

        Args:
            iban (int): The bank account identifier to get.

        Raises:
            KeyError: If the account does not exist in the database.

        Returns:
            Account: The user account with the given IBAN.
        """
        account = None
        with shelve.open(self._database) as accounts:
            if str(iban) not in accounts:
                raise KeyError("Account does not exist")
            account = accounts[str(iban)]
        return account

    def login(self, iban: int) -> Account:
        """Authenticate a user logging into an ATM.

        Args:
            iban (int): The bank account identifier of the user.

        Raises:
            BankError: If the authentication fails.

        Returns:
            Account: The user's account.
        """
        if iban not in self:
            raise BankError("User authentication failed")
        return self.get_account(iban)

    def valid_user(self, user: Account) -> bool:
        """Checks whether the given user data matches the database.

        Args:
            user (Account): The user account to validate.

        Returns:
            bool: True if the account matches the database, False otherwise.
        """
        validated = False
        account = self.get_account(user.iban)
        if user == account:
            validated = True
        return validated

    def check_balance(self, user: Account) -> float:
        """Get the given user's account balance.

        Args:
            user (Account): The account to get the balance of.

        Raises:
            BankError: If the user data has been tampered with.

        Returns:
            float: The user's account balance.
        """
        if not self.valid_user(user):
            raise BankError("User data has been tampered with")
        account = self.get_account(user.iban)
        return account.balance

    def withdraw(self, user: Account, amount: float):
        """Withdraw the given amount from the user's account.

        Args:
            user (Account): The account to withdraw from.
            amount (float): The amount to withdraw.

        Raises:
            TypeError: If the amount isn't a float or an int.
            ValueError: If the amount is not greater than 0.
            BankError: If the user's data has been tampered with.
            AccountError: If the user doesn't have sufficient balance.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Must be of type int or float")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not self.valid_user(user):
            raise BankError("User data has been tampered with")
        with shelve.open(self._database) as accounts:
            account = accounts[str(user.iban)]
            try:
                account.withdraw(amount)
            except AccountError as error:
                raise AccountError() from error
            accounts[str(user.iban)] = account

    def deposit(self, user: Account, amount: float):
        """Deposit the given amount into the user's account.

        Args:
            user (Account): The account to deposit into
            amount (float): The amount to deposit.

        Raises:
            TypeError: If the amount isn't a float or an int.
            ValueError: If the amount is not greater than 0.
            BankError: If the user's data has been tampered with.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Must be of type int or float")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not self.valid_user(user):
            raise BankError("User data has been tampered with")
        with shelve.open(self._database) as accounts:
            account = accounts[str(user.iban)]
            account.deposit(amount)
            accounts[str(user.iban)] = account

    def create_account(self, name: str, pin: int) -> int:
        """Add a user to the bank and return their bank account number (IBAN).

        Args:
            name (str): The user's name.
            pin (int): The 4 digit pin for logging into an ATM.

        Returns:
            int: The users bank account number (IBAN).
        """
        iban = self._next_iban
        account = Account(iban, name, pin)
        with shelve.open(self._database) as accounts:
            accounts[str(iban)] = account
        self._next_iban += 1
        return iban

    def create_admin_account(self, name: str, pin: int) -> int:
        """Add an admin to the bank and return their account number (IBAN).

        Args:
            name (str): The admin's name.
            pin (int): The 4 digit pin for logging into an ATM.

        Returns:
            int: The admin's bank account number (IBAN).
        """
        iban = self._next_iban
        account = Account(iban, name, pin, True)
        with shelve.open(self._database) as accounts:
            accounts[str(iban)] = account
        self._next_iban += 1
        return iban

    def check_admin(self, user: Account) -> bool:
        """Check if the user is an admin in the database.

        Args:
            user (Account): The account to check.

        Raises:
            BankError: If the users data has been tampered with.

        Returns:
            bool: True if the user is an admin, otherwise False.
        """
        if not self.valid_user(user):
            raise BankError("User data has been tampered with")
        account = self.get_account(user.iban)
        return account.admin
