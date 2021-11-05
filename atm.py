from account import Account

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
        elif account.balance > self.balance:
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

    def transfter_user(self,account,account1,amount):
        print('conor and alex please do your bank class xxxxxxx')
    
            

atm = ATM()
user = Account(1,4323,'wegwe')
print(user)
user.deposit(1000)
print(atm.withdraw_user(user,500))
print(user.balance)
print(atm.deposit_user(user,500))
print(atm.deposit_user(user,500))
print(atm.balance)
