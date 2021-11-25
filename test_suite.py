from atm import ATM
from bank import Bank
from exceptions import BankError,AccountError,AtmError
from main import *

import unittest
import pytest


''' WhiteBox Testing for Withdraw Bank'''
class WithdrawAIBTesting(unittest.TestCase):
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




'''Admin Deposit Whitebox Testing'''

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


'''Admin Withdraw Whitebox Testing'''

class AdminWithdrawTestClass(unittest.TestCase):
    def setup(self, balance: float = 1000.0):
        aib = Bank("aib", "Allied Irish Banks")

        user_iban = aib.create_account("User", 1234)
        admin_iban = aib.create_admin_account("Admin", 1010)

        aib_atm = ATM(aib, balance)
        return aib_atm, user_iban, admin_iban
    
    def test_admin_correct_amount_float(self):
        start_balance = 1000.0
        atm, user_iban, admin_iban = self.setup(start_balance)
        admin = atm.login(admin_iban)

        amount = 100.0
        atm.admin_withdraw(admin, amount)
        assert atm._balance == start_balance - amount

    def test_admin_correct_amount_int(self):
        start_balance = 1000.0
        atm, user_iban, admin_iban = self.setup(start_balance)
        admin = atm.login(admin_iban)

        amount = 100
        atm.admin_withdraw(admin, amount)
        assert atm._balance == start_balance - amount

    def test_admin_incorrect_amount(self):
        start_balance = 10.0
        atm, user_iban, admin_iban = self.setup(start_balance)
        admin = atm.login(admin_iban)

        amount = 100.0
        with pytest.raises(AtmError):
            atm.admin_withdraw(admin, amount)

    def test_admin_incorrect_type(self):
        atm, user_iban, admin_iban = self.setup()
        admin = atm.login(admin_iban)

        amount = "100"
        with pytest.raises(TypeError):
            atm.admin_withdraw(admin, amount)

    def test_incorrect_account(self):
        atm, user_iban, admin_iban = self.setup()

        account = BankDepositTests()
        with pytest.raises(TypeError):
            atm.admin_withdraw(account, amount=100.0)

    def test_admin_invalid_amount(self):
        atm, user_iban, admin_iban = self.setup()
        admin = atm.login(admin_iban)

        amount = -10000000000
        with pytest.raises(ValueError):
            atm.admin_withdraw(admin, amount)

    def test_user(self):
        atm, user_iban, admin_iban = self.setup()
        user = atm.login(user_iban)

        with pytest.raises(AccountError):
            atm.admin_withdraw(user, 100)

    def test_user_incorrect_type(self):
        atm, user_iban, admin_iban = self.setup()
        user = atm.login(user_iban)

        with pytest.raises(TypeError):
            atm.admin_withdraw(user, "100")


    

if __name__ == '__main__':
    unittest.main()



