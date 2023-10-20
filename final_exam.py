from abc import ABC, abstractmethod

class Account(ABC):
    accounts = []
    loans = {}
    
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = len(Account.accounts) + 1
        self.balance = 0
        self.transactions = []
        Account.accounts.append(self)

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            self.transactions.append(f"Deposited ${amount}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if amount >= 0 and amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrew ${amount}")
        else:
            print("Withdrawal amount exceeded")

    def check_balance(self):
        print(f"Available balance: ${self.balance}")

    def check_transactions(self):
        for transaction in self.transactions:
            print(transaction)

    def take_loan(self):
        if self.allow_loan:
            if self.account_number in Account.loans:
                if Account.loans[self.account_number] < 2:
                    loan_amount = float(input("Enter the loan amount: $"))
                    if loan_amount > 0:
                        self.balance += loan_amount
                        self.transactions.append(f"Loan received: ${loan_amount}")
                        Account.loans[self.account_number] += 1
                        print(f"Loan received: ${loan_amount}")
                    else:
                        print("Invalid loan amount. Loan amount should be greater than 0.")
                else:
                    print("You can't take more loans.")
            else:
                Account.loans[self.account_number] = 1
                loan_amount = float(input("Enter the loan amount: $"))
                if loan_amount > 0:
                    self.balance += loan_amount
                    self.transactions.append(f"Loan received: ${loan_amount}")
                    print(f"Loan received: ${loan_amount}")
                else:
                    print("Invalid loan amount. Loan amount should be greater than 0.")
        else:
            print("Loan feature is currently disabled by the admin.")


    def transfer(self, recipient_account, amount):
        if amount > 0 and amount <= self.balance:
            if recipient_account <= len(Account.accounts):
                recipient = Account.accounts[recipient_account - 1]
                recipient.deposit(amount)
                self.withdraw(amount)
                self.transactions.append(f"Transferred ${amount} to Account {recipient.account_number}")
                recipient.transactions.append(f"Received ${amount} from Account {self.account_number}")
            else:
                print("Recipient account does not exist")
        else:
            print("Insufficient balance for transfer")


    @abstractmethod
    def show_info(self):
        pass

class SavingsAccount(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "Savings")

    def show_info(self):
        print(f"Account Type: {self.account_type}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: ${self.balance}")

class CurrentAccount(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, "Current")

    def show_info(self):
        print(f"Account Type: {self.account_type}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Address: {self.address}")
        print(f"Account Number: {self.account_number}")
        print(f"Current Balance: ${self.balance}")

class Admin:
    def create_account(self, name, email, address, account_type):
        if account_type == "Savings":
            account = SavingsAccount(name, email, address)
        elif account_type == "Current":
            account = CurrentAccount(name, email, address)
        else:
            print("Invalid account type")

    def delete_account(self, account_number):
        if account_number - 1 < len(Account.accounts):
            deleted_account = Account.accounts.pop(account_number - 1)
            del Account.loans[deleted_account.account_number]
            print(f"Account {account_number} deleted")

    def see_all_accounts(self):
        for account in Account.accounts:
            account.show_info()
            print()

    def total_available_balance(self):
        total_balance = sum(account.balance for account in Account.accounts)
        print(f"Total Available Balance: ${total_balance}")

    def total_loan_amount(self):
        total_loan = sum(Account.loans.values()) * 500
        print(f"Total Loan Amount: ${total_loan}")

    def toggle_loan_feature(self, enable):
        Account.allow_loan = enable

# Main program
admin = Admin()
admin.toggle_loan_feature(True)

while True:
    print("\nChoose your role:")
    print("1. User")
    print("2. Admin")
    print("3. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        print("\nUser Menu:")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        user_choice = int(input("Enter your choice: "))

        if user_choice == 1:
            name = input("Name: ")
            email = input("Email: ")
            address = input("Address: ")
            print("Choose Account Type: ")
            print("1. Savings")
            print("2. Current")
            account_type_choice = int(input("Enter your choice: "))
            if account_type_choice == 1:
                admin.create_account(name, email, address, "Savings")
            elif account_type_choice == 2:
                admin.create_account(name, email, address, "Current")
            else:
                print("Invalid choice")

        elif user_choice == 2:
            account_number = int(input("Enter your account number: "))
            if account_number - 1 < len(Account.accounts):
                user_account = Account.accounts[account_number - 1]
                while True:
                    print("\nUser Menu:")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Check Transactions")
                    print("5. Take Loan")
                    print("6. Transfer Money")
                    print("7. Logout")
                    user_option = int(input("Enter your choice: "))
                    if user_option == 1:
                        amount = float(input("Enter the deposit amount: $"))
                        user_account.deposit(amount)
                    elif user_option == 2:
                        amount = float(input("Enter the withdrawal amount: $"))
                        user_account.withdraw(amount)
                    elif user_option == 3:
                        user_account.check_balance()
                    elif user_option == 4:
                        user_account.check_transactions()
                    elif user_option == 5:
                        user_account.take_loan()
                    elif user_option == 6:
                        recipient_account = int(input("Enter recipient's account number: "))
                        amount = float(input("Enter the transfer amount: $"))
                        user_account.transfer(recipient_account, amount)
                    elif user_option == 7:
                        break
                    else:
                        print("Invalid choice")

        elif user_choice == 3:
            break

    elif choice == 2:
        print("\nAdmin Menu:")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. See All Accounts")
        print("4. Total Available Balance")
        print("5. Total Loan Amount")
        print("6. Toggle Loan Feature")
        print("7. Logout")
        admin_option = int(input("Enter your choice: "))
        if admin_option == 1:
            name = input("Name: ")
            email = input("Email: ")
            address = input("Address: ")
            print("Choose Account Type: ")
            print("1. Savings")
            print("2. Current")
            account_type_choice = int(input("Enter your choice: "))
            if account_type_choice == 1:
                admin.create_account(name, email, address, "Savings")
            elif account_type_choice == 2:
                admin.create_account(name, email, address, "Current")
            else:
                print("Invalid choice")
        elif admin_option == 2:
            account_number = int(input("Enter account number to delete: "))
            admin.delete_account(account_number)
        elif admin_option == 3:
            admin.see_all_accounts()
        elif admin_option == 4:
            admin.total_available_balance()
        elif admin_option == 5:
            admin.total_loan_amount()
        elif admin_option == 6:
            enable_loan = input("Enable (Y) or Disable (N) the loan feature: ")
            if enable_loan.lower() == "y":
                admin.toggle_loan_feature(True)
            elif enable_loan.lower() == "n":
                admin.toggle_loan_feature(False)
            else:
                print("Invalid choice")
        elif admin_option == 7:
            break

    elif choice == 3:
        break
