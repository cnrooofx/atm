"""A user account for a bank."""

from exceptions import AccountError

class Account:
    """An account for a bank containing the user details."""

    def __init__(self, iban: int, name: str, pin: int, admin: bool = False):
        """Create a new account.

        Args:
            iban (int): The bank account identifier of the account.
            name (str): The user's name.
            pin (int): The user's PIN to authenticate at an ATM.
            admin (bool, optional): User's admin status. Defaults to False.
        """
        self._iban = iban
        self._name = name
        self._pin = pin
        self._admin = admin
        self._balance = 0

    def __str__(self) -> str:
        """Return a string representation of the account."""
        string = f"""IBAN: {self._iban}\
                   \nName: {self._name}\
                   \nBalance: {self._balance}\n"""
        if self._admin:
            string += "---Admin Account---\n"
        return string

    def __eq__(self, other) -> bool:
        """Check if two account objects have the same account data.

        Args:
            other (Account): The other account to compare.

        Raises:
            TypeError: If trying to compare with something other than Account.

        Returns:
            bool: True if the two accounts are the same, False otherwise.
        """
        if not isinstance(other, Account):
            raise TypeError("Must compare with another account.")
        outcome = False
        if self._iban == other.iban and self._name == other.name\
           and self._admin == other.admin and self._balance == other.balance\
           and other.check_pin(self._pin):
            outcome = True
        return outcome

    @property
    def iban(self):
        """Get the user's IBAN."""
        return self._iban

    @property
    def name(self):
        """Get the user's name."""
        return self._name

    @property
    def admin(self):
        """Return whether the user is an admin or not."""
        return self._admin

    @property
    def balance(self):
        """Get the user's account balance."""
        return self._balance

    def deposit(self, amount: float):
        """Deposit the given amount into the account.

        Args:
            amount (float): The amount to deposit

        Raises:
            TypeError: If the amount is not a float or an int.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Must be of type int or float")
        self._balance += amount

    def withdraw(self, amount: float):
        """Withdraw the given amount from the account.

        Args:
            amount (float): The amount to withdraw.

        Raises:
            TypeError: If the amount is not a float or an int.
            AccountError: If the account does not have sufficient balance.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Must be of type int or float")
        if amount > self._balance:
            raise AccountError("Insufficient funds")
        self._balance -= amount

    def check_pin(self, pin: int) -> bool:
        """Check whether the given PIN matches the one on the account.

        Args:
            pin (int): The PIN to check.

        Returns:
            bool: True if the PINs are the same, otherwise False.
        """
        pin_equal = False
        if pin == self._pin:
            pin_equal = True
        return pin_equal

    def update_pin(self, new_pin: int):
        """Update the user's PIN.

        Args:
            new_pin (int): The new PIN.

        Raises:
            ValueError: If the PIN is not exactly 4 digits long.
        """
        if len(new_pin) != 4:
            raise ValueError("Pin length must be 4.")
        self._pin = int(new_pin)
