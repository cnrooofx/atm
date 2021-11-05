import shelve
class Bank:
    def __init__(self,bank_name):
        self.bank_name = bank_namei
        self.accounts = shelve.open("bank_accounts")

    def __str__(self):
        return str(self.bank_name)

    def find_account(self,acc_num):
        shelf = shelve.open("bank_accounts")
        acc = self.accounts.get(str(acc_num))
        shelf.close()
        if acc != None:
            return acc
        raise Exception("Error! Account number does not exist")

   
        
