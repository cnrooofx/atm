from exceptions import BankError
from bank import Bank
from account import Account
import unittest


class BankDepositTests(unittest.TestCase):
    def setUp(self):
        self.bank1 = Bank("aib","AIB")
        iban = self.bank1.create_account(1234,"Conor")
        self.account = self.bank1.get_account(iban)
        self.invalidAccount = "Fake_ACCOUNT"

    
    def test_invalid_amount_type(self):
        with self.assertRaises(TypeError):
            self.bank1.deposit(self.account,"HELLO_WORLD")

    def test_invalid_amount_value(self):
        with self.assertRaises(ValueError):
            self.bank1.deposit(self.account,-50)

    def test_invalid_account(self):
        with self.assertRaises(BankError):
            self.bank1.deposit(self.invalidAccount,50)


if __name__ == "__main__":
    unittest.main()



