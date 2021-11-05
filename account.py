class Account:
    def __init__(self,number,pin,email):
        self.number = number
        self.balance = 0
        self.pin = pin
        self.email = email

    @property
    def balance(self):
        return self._balance

    @balance.setter 
    def balance(self,x):
        if not isinstance(x, int) and not isinstance(x, float):
            raise ValueError("ERROR: NUMBER INPUT REQUIRED")
        elif x < 0:
            raise Exception("ERROR: NUMBER IS NOT GREATER THAN 0")
        else: 
            self._balance = x

    @property
    def pin(self):
        return self._pin

    @pin.setter
    def pin(self, newPin):
        try:
            if len(newPin) == 4:
                self._pin = int(newPin)
            else:
                raise ValueError("PIN_Error(Length)")
        except TypeError:
            return "PIN_Error(Type)"

    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self,value):
        self._number = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self,newEmail):
        self._email = newEmail


    def deposit(self,val):
        self.balance += val

    def withdraw(self,val):
        if self._balance >= val:
            self.balance -= val
        else:
            raise Exception("ERROR: NOT ENOUGH BALANCE")

    
    
  



    



