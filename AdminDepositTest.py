import unittest
from account import Account
from exceptions import AccountError

from main import *

class TestAdminDeposit(unittest.TestCase):
    def setUp(self) -> None:
        self.aib_atm, self.iban_list = setup()
        self.user = self.aib_atm.login(5)

    def testInvalidAccountRaisesTypeError(self):
        with self.assertRaises(TypeError):
            self.aib_atm.admin_deposit('account', 100)

    def testInvalidAmountRaisesTypeError(self):
        with self.assertRaises(TypeError):
            self.user = self.aib_atm.login(5)
            self.aib_atm.admin_deposit(self.user, 'one hundo')

    def testNegativeAmountRaisesValueError(self):
        with self.assertRaises(ValueError):
            self.user = self.aib_atm.login(5)
            self.aib_atm.admin_deposit(self.user, -100)
    
    def testNonAdminUserRaisesAccountError(self):
        with self.assertRaises(AccountError):
            self.user = self.aib_atm.login(1)
            self.aib_atm.admin_deposit(self.user, 100)
    
    def testValidAccountAndAmountPass(self):
        self.user = self.aib_atm.login(5)
        startingBalance = self.aib_atm._balance
        topUpAmount = 100
        self.aib_atm.admin_deposit(self.user, topUpAmount)
        self.assertEqual(startingBalance+topUpAmount, self.aib_atm.check_balance(self.user))

if __name__ == '__main__':
    unittest.main()
