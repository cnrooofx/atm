from bank import Bank
from account import Account
from exceptions import AtmError, AccountError


class ATM:
    """An Automated Teller Machine for user transactions with a bank."""

    def __init__(self, bank: Bank, balance: float = 1000.0):
        self._bank = bank
        self._balance = balance
        self._connected_banks = {}

    def __str__(self):
        return f"ATM for {self._bank.name}"

    def login(self, iban: int):
        return self._bank.login(iban)

    def user_check_balance(self, account: Account):
        return self._bank.check_balance(account)

    def user_withdraw(self, account: Account, amount: float):
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
        except AccountError as e:
            raise AccountError() from e

    def user_deposit(self, account: Account, amount: float):
        if not isinstance(account, Account):
            raise TypeError("Not a valid user")
        if not isinstance(amount, (int, float)):
            raise TypeError("Must be of type int or float")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self._bank.deposit(account, amount)
        self._balance += amount

    # def user_transfer(self, account: Account, amount: float, payee_iban: int,
    #                   payee_bank: str):
    #     if isinstance(account, Account) and isinstance(payee, Account):
    #         if amount > self._balance:
    #             raise AtmError("ATM does not have enough funds")
    #         self._balance -= amount
    #         payee_bank.transfer_funds(account, payee, amount)

    def admin_withdraw(self, account: Account, amount: float):
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
        self._balance += amount

    def check_balance(self, account: Account) -> float:
        if not isinstance(account, Account):
            raise TypeError("Not a valid user")
        if not self._bank.check_admin(account):
            raise AccountError("User must be an admin")
        return self._balance

    def add_connected_bank(self, bank: Bank) -> bool:
        """Add a bank connection to this ATM.

        Allows ATM users to transfer funds to other users the added bank.

        Args:
            bank (Bank): The new bank to be added

        Raises:
            TypeError: If the bank isn't from the Bank class

        Returns:
            bool: True if the bank was added, otherwise False
        """
        added = False
        if not isinstance(bank, Bank):
            raise TypeError("Not a valid bank")
        elif bank is not self._bank:
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

def main():
    aib = Bank("aib_test", "Allied Irish Banks (Test)")
    aib_atm = ATM(aib)

    aib.create_account("a1", "email1", 1234)


if __name__ == "__main__":
    main()
