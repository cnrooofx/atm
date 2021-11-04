class Account:
    def __init__(self,number,pin,email):
        self._number = number
        self._balance = 0
        self._pin = pin
        self._email = email

    def getBalance(self):
        return self._balance

    def getPin(self):
        return self._pin

    def getNumber(self):
        return self._number
    
    def getEmail(self):
        return self._email

    def setPin(self,newPin):
        try:
            if len(newPin) == 4:
                self._pin = int(newPin)
            else:
                return "PIN_Error(Length)"
        except TypeError:
            return "PIN_Error(Type)"

    def setEmail(self,newEmail):
        self._email = newEmail


    def deposit(self,val):
        self._balance += val

    def withdraw(self,val):
        if self._balance >= val:
            self._balance -= val
        else:
            return "Error"

    
    
  



    



