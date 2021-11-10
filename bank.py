from account import Account
import shelve

from exceptions import BankError, AccountError


class Bank:
    def __init__(self, bank_id: str, bank_name: str):
        """Initialise a new Bank.

        Args:
            bank_id (str): Short identifier for the bank (Must have no spaces)
            bank_name (str): Longer name of the bank for printing strings
        """
        self._name = bank_name
        self._database = f"{bank_id}_bank_accounts"
        self._next_iban = 1

    def __str__(self) -> str:
        return str(self._name)

    def __contains__(self, iban: int) -> bool:
        """Returns whether or not the account is in this bank.

        Args:
            iban (int): The IBAN of the account to check

        Returns:
            bool: True if the account is in the bank, otherwise False
        """
        contained = False
        with shelve.open(self._database) as accounts:
            if str(iban) in accounts:
                contained = True
        return contained

    @property
    def name(self):
        return self._name

    def get_account(self, iban: int) -> Account:
        with shelve.open(self._database) as accounts:
            if str(iban) not in accounts:
                raise KeyError("Account does not exist")
            account = accounts[str(iban)]
        return account

    def login(self, iban: int) -> Account:
        if iban in self:
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
        if not self.valid_user(user):
            raise BankError("User data has been tampered with")
        account = self.get_account(user.iban)
        return account.balance

    def withdraw(self, user: Account, amount: float):
        """Withdraw the given amount from the user's account.

        Args:
            user (Account): The user account to withdraw from.
            amount (float): The amount to withdraw

        Raises:
            TypeError: [description]
            BankError: [description]
            AccountError: [description]
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
            except AccountError as e:
                raise AccountError() from e
            accounts[str(user.iban)] = account

    def deposit(self, user: Account, amount: float):
        """Deposit the given amount into the user's account.

        Args:
            user (Account): The user account to deposit into.
            amount (float): The amount of the deposit.

        Raises:
            TypeError: If the amount is not a float or an int.
            BankError: If the users data has been tampered with.
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

    # def transfer_funds(self, account, payee, ammount):
    #     with shelve.open(self._database) as accounts:
    #         current_iban = str(account.iban)
    #         payee_iban = str(payee.iban)
    #         current_account = accounts.get(current_iban)
    #         payee_account = accounts.get(payee_iban)

    #         if current_account is None or payee_account is None:
    #             raise KeyError("Account does not exist")
    #         account.balance -= ammount
    #         payee.balance += ammount
    #         accounts[current_iban] = account
    #         accounts[payee_iban] = payee

    def create_account(self, name: str, email: str, pin: int) -> int:
        """Add a user to the bank and return their bank account number (IBAN).

        Args:
            name (str): The user's name
            email (str): The user's email
            pin (int): The 4 digit pin for logging into an ATM

        Returns:
            int: The users bank account number (IBAN)
        """
        iban = self._next_iban
        account = Account(iban, name, email, pin)
        with shelve.open(self._database) as accounts:
            accounts[str(iban)] = account
        self._next_iban += 1
        return iban

    def create_admin_account(self, name: str, email: str, pin: int) -> int:
        """Add an admin to the bank and return their account number (IBAN).

        Args:
            name (str): The admin's name
            email (str): The admin's email
            pin (int): The 4 digit pin for logging into an ATM

        Returns:
            int: The admin's bank account number (IBAN)
        """
        iban = self._next_iban
        account = Account(iban, name, email, pin, admin=True)
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


def main():
    aib = Bank("aib_test", "Allied Irish Banks")
    user1 = aib.create_account("User 1", "email1", 1234)
    print(user1 in aib)
    user1_account = aib.get_account(user1)
    print(user1_account)


if __name__ == "__main__":
    main()
