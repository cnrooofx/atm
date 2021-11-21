from atm import ATM
from bank import Bank
from exceptions import BankError,AccountError
import unittest

class MyTestCase(unittest.TestCase):
    ''' WhiteBox Testing'''
    def test_withdraw_type(self):
        aib = Bank("aib", "Allied Irish Banks")
        user1 = aib.create_account("Aidan", 1234)
        acc = aib.get_account(1)
        self.assertRaises(TypeError, aib.withdraw, acc, 'mfif')

    def test_withdraw_value(self):
        aib = Bank("aib", "Allied Irish Banks")
        user1 = aib.create_account("Aidan", 1234)
        acc = aib.get_account(1)
        self.assertRaises(ValueError, aib.withdraw, acc, -10)

 
    def test_withdraw_user(self):
        aib = Bank("aib", "Allied Irish Banks")
        user1 = aib.create_account("Aidan", 1234)
        self.assertRaises(BankError, aib.withdraw, 'fewf', 10)

    def test_withdraw_amount(self):
        aib = Bank("aib", "Allied Irish Banks")
        user2 = aib.create_account("Aidan", 1234)
        acc = aib.get_account(1)
        self.assertRaises(AccountError, aib.withdraw, acc, 100)


if __name__ == '__main__':


    unittest.main()



