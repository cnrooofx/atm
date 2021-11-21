"""Install pytest with `pip3 install pytest`

Run tests with `python3 -m pytest test_admin_withdraw.py`
"""

import pytest

from bank import Bank
from atm import ATM
from exceptions import AccountError, AtmError


def setup(balance: float = 1000.0):
    aib = Bank("aib", "Allied Irish Banks")

    user_iban = aib.create_account("User", 1234)
    admin_iban = aib.create_admin_account("Admin", 1010)

    aib_atm = ATM(aib, balance)
    return aib_atm, user_iban, admin_iban


class TestClass:
    pass


def test_admin_correct_amount_float():
    start_balance = 1000.0
    atm, user_iban, admin_iban = setup(start_balance)
    admin = atm.login(admin_iban)

    amount = 100.0
    atm.admin_withdraw(admin, amount)
    assert atm._balance == start_balance - amount

def test_admin_correct_amount_int():
    start_balance = 1000.0
    atm, user_iban, admin_iban = setup(start_balance)
    admin = atm.login(admin_iban)

    amount = 100
    atm.admin_withdraw(admin, amount)
    assert atm._balance == start_balance - amount

def test_admin_incorrect_amount():
    start_balance = 10.0
    atm, user_iban, admin_iban = setup(start_balance)
    admin = atm.login(admin_iban)

    amount = 100.0
    with pytest.raises(AtmError):
        atm.admin_withdraw(admin, amount)

def test_admin_incorrect_type():
    atm, user_iban, admin_iban = setup()
    admin = atm.login(admin_iban)

    amount = "100"
    with pytest.raises(TypeError):
        atm.admin_withdraw(admin, amount)

def test_incorrect_account():
    atm, user_iban, admin_iban = setup()

    account = TestClass()
    with pytest.raises(TypeError):
        atm.admin_withdraw(account, amount=100.0)

def test_admin_invalid_amount():
    atm, user_iban, admin_iban = setup()
    admin = atm.login(admin_iban)

    amount = -10000000000
    with pytest.raises(ValueError):
        atm.admin_withdraw(admin, amount)

def test_user():
    atm, user_iban, admin_iban = setup()
    user = atm.login(user_iban)

    with pytest.raises(AccountError):
        atm.admin_withdraw(user, 100)

def test_user_incorrect_type():
    atm, user_iban, admin_iban = setup()
    user = atm.login(user_iban)

    with pytest.raises(TypeError):
        atm.admin_withdraw(user, "100")
