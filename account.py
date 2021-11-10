from exceptions import AccountError

class Account:
    def __init__(self, iban: int, name: str, email: str, pin: int,
                 admin: bool = False):
        self._iban = iban
        self._name = name
        self._email = email
        self._pin = pin
        self._admin = admin
        self._balance = 0

    def __str__(self) -> str:
        string = f"""IBAN: {self._iban}\
                   \nName: {self._name}\
                   \nEmail: {self._email}\
                   \nBalance: {self._balance}\n"""
        if self._admin:
            string += "---Admin Account---\n"
        return string

    def __eq__(self, other) -> bool:
        if not isinstance(other, Account):
            raise TypeError("Must compare with another account.")
        outcome = False
        if self._iban == other.iban and self._name == other.name\
           and self._email == other.email and self._pin == other.pin\
           and self._admin == other.admin and self._balance == other.balance:
            outcome = True
        return outcome

    @property
    def iban(self):
        return self._iban

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def pin(self):
        return self._pin

    @property
    def admin(self):
        return self._admin

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount: float):
        if not isinstance(amount, (int, float)):
            raise TypeError("Must be of type int or float")
        self._balance += amount

    def withdraw(self, amount: float):
        if not isinstance(amount, (int, float)):
            raise TypeError("Must be of type int or float")
        if amount > self._balance:
            raise AccountError("Insufficient funds")
        self._balance -= amount

    def update_pin(self, new_pin: int):
        if len(new_pin) != 4:
            raise ValueError("Pin length must be 4.")
        self._pin = int(new_pin)


def main():
    print("String Test\n-----------")
    a1 = Account(1234, "Test", "test", 0000)
    print(a1)
    admin = Account(4567, "Admin", "admin@aib.ie", 1234, True)
    print(admin)


if __name__ == "__main__":
    main()
