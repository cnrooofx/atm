from account import Account
from bank import Bank

class ATM:
    def __init__(self):
        self.balance = 1000

    @property
    def balance(self):
        return self._balance

    @balance.setter 
    def balance(self,amount):
        if not isinstance(amount, int) and not isinstance(amount, float):
            raise ValueError("ERROR: NUMBER INPUT REQUIRED")
        elif amount < 0:
            raise Exception("ERROR: NUMBER IS NOT GREATER THAN 0")
        else: 
            self._balance = amount

    def withdraw_user(self, account, amount):
        if not isinstance(amount, int) and not isinstance(amount, float):
            raise ValueError("ERROR: NUMBER INPUT REQUIRED")
        elif amount > self.balance:
            raise Exception("ERROR: ATM TOO SHORT FUNDS")
        else:
            account.withdraw(amount)
            self.balance -= amount
            return('Success')

    def deposit_user(self, account, amount):
        if not isinstance(amount, int) and not isinstance(amount, float):
            raise ValueError("ERROR: NUMBER INPUT REQUIRED")
        else:
            account.deposit(amount)
            self.balance += amount
            return('Success')

    def transfter_user(self,bank,payer,payee,amount):
        if isinstance(payer, Account) and isinstance(payee, Account):
            if amount <= self.balance:
                self.balance -= amount
                bank.transfer_funds(payer,payee,amount)
                return('Success')
            else:
                raise Exception("ERROR: ATM TOO SHORT FUNDS")

    def admin_withdraw(self,account,amount):
        if not isinstance(account,Account):
            raise Exception("ERROR: Not a valid user")
        elif not account.get_admin():
            raise Exception("ERROR: User is not an admin")
        elif amount > self.balance:
            raise ValueError("ERROR: ATM SHORT ON FUNDS")
        else:
            self.balance-= amount
            
    def admin_deposit(self,account,amount):
        if not isinstance(account,Account):
            raise Exception("ERROR: Not a valid user")
        elif not account.get_admin():
            raise Exception("ERROR: User is not an admin")
        elif amount > self.balance:
            raise ValueError("ERROR: ATM SHORT ON FUNDS")
        else:
            self.balance += amount

    def check_balance(self):
        return self.balance
    
'''
atm = ATM()
bank = Bank('AIB')
user = Account(1,4323,'wegwe',bank)
user1 = Account(2,4323,'wegwe',bank)
print(user)
user.deposit(1000)
user1.deposit(1000)
print(atm.withdraw_user(user,500))
print(user.balance)
print(atm.deposit_user(user,500))
print(atm.deposit_user(user,500))
print(atm.balance)
print(atm.transfter_user(bank,user,user1,1000))
print(atm.transfter_user(bank,user,user1,500))
print(atm.balance)
'''