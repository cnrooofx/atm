import shelve
class Bank:
    def __init__(self,bank_name):
        self.bank_name = bank_name
        self.accounts = shelve.open("bank_accounts")

    def __str__(self):
        return str(self.bank_name)

    def find_account(self,acc_num):
        shelf = self.accounts
        acc = self.accounts.get(str(acc_num))
        if acc != None:
            return acc
        raise Exception("Error! Account number does not exist")

    def update_shelf(self,acc):
        accounts = self.accounts
        print(accounts[str(acc.number)])
        accounts[str(acc.number)] = str(acc)
        accounts.sync()
        return 

    def transfer_funds(self,payer,payee,ammount):
        acc1 = self.accounts.get(str(payer.number))
        acc2 = self.accounts.get(str(payee.number))
        if acc1 != None and acc2 != None:
            payer.balance -= ammount
            payee.balance += ammount
            self.update_shelf(payer)
            self.update_shelf(payee)
        else:
            raise Exception("ERROR! Accounts not registered in bank")




