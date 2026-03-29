 #  Using OOP 
# This program allows a user to:
# 1. Register as a new customer
# 2. Login using Customer ID and PIN
# 3. Deposit money
# 4. Withdraw money
# 5. Check balance
# 6. View customer details
# All customer data is stored in a file so multiple users can use the system.

import datetime
import random
import re
import os

# File where customer data will be saved
FILE_NAME = "customers.txt"
# Customer class stores all customer information and banking operations
class Customer:
    def __init__(self, cust_id, name, contact, pan, pin, balance=0):
        self.cust_id = cust_id      # unique customer ID
        self.name = name            # customer name
        self.contact = contact      # 10 digit mobile number
        self.pan = pan              # PAN number
        self.pin = pin              # 4 digit security PIN
        self.balance = balance      # account balance
    # Function to deposit money
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print("Deposit successful")
            self.log_transaction("DEPOSIT", amount)
        else:
            print("Invalid amount")

    # Function to withdraw money
    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount")
        elif amount > self.balance:
            print("Insufficient balance")
        else:
            self.balance -= amount
            print("Withdrawal successful")
            self.log_transaction("WITHDRAW", amount)
    # Function to show current balance
    def show_balance(self):
        print("Current balance:", self.balance)
    # Function to show customer details
    def show_details(self):
        print("Customer ID:", self.cust_id)
        print("Name:", self.name)
        print("Contact:", self.contact)
        print("PAN:", self.pan)
        print("Balance:", self.balance)
    # Function to save each transaction in a separate file with date and time
    def log_transaction(self, action, amount):
        with open("transactions.txt", "a") as file:
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(
                f"{time},ID:{self.cust_id},Name:{self.name},{action},Amount:{amount},Balance:{self.balance}\n"
            )
# Function to save a new customer into the file
def save_customer(customer):
    with open(FILE_NAME, "a") as file:
        file.write(
            f"{customer.cust_id},{customer.name},{customer.contact},{customer.pan},{customer.pin},{customer.balance}\n"
        )
# Function to load all customers from file into dictionary
def load_customers():
    customers = {}
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                cust_id, name, contact, pan, pin, balance = line.strip().split(",")
                customers[cust_id] = Customer(
                    cust_id, name, contact, pan, pin, float(balance)
                )
    return customers
# Function to update file after deposit or withdrawal
def update_file(customers):
    with open(FILE_NAME, "w") as file:
        for cust in customers.values():
            file.write(
                f"{cust.cust_id},{cust.name},{cust.contact},{cust.pan},{cust.pin},{cust.balance}\n"
            )
# Function to check contact number is exactly 10 digits
def valid_contact(contact):
    return contact.isdigit() and len(contact) == 10
# Function to check PAN format (Example: ABCDE1234F)
def valid_pan(pan):
    return re.match(r"[A-Z]{5}[0-9]{4}[A-Z]", pan)
# Function for new customer registration
def register(customers):
    print("New Customer Registration")

    name = input("Enter Name: ")

    contact = input("Enter Contact (10 digits): ")
    if not valid_contact(contact):
        print("Invalid contact number")
        return
    pan = input("Enter PAN (ABCDE1234F): ").upper()
    if not valid_pan(pan):
        print("Invalid PAN format")
        return
    pin = input("Set 4 digit PIN: ")
    if not (pin.isdigit() and len(pin) == 4):
        print("PIN must be 4 digits")
        return
    # Generate random customer ID
    cust_id = str(random.randint(10000, 99999))
     # Create new customer object
    customer = Customer(cust_id, name, contact, pan, pin)
   # Store in dictionary and file
    customers[cust_id] = customer
    save_customer(customer)
    print("Registration successful")
    print("Your Customer ID:", cust_id)
# Function for customer login
def login(customers):
    print("Customer Login")
    cust_id = input("Enter Customer ID: ")
    pin = input("Enter PIN: ")
    if cust_id in customers and customers[cust_id].pin == pin:
        print("Login successful")
        print("Welcome", customers[cust_id].name)
        return customers[cust_id]
    else:
        print("Invalid ID or PIN")
        return None
# Banking menu shown after successful login
def banking_menu(customer, customers):
    while True:
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. View Details")
        print("5. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            amount = float(input("Enter amount: "))
            customer.deposit(amount)

        elif choice == "2":
            amount = float(input("Enter amount: "))
            customer.withdraw(amount)

        elif choice == "3":
            customer.show_balance()

        elif choice == "4":
            customer.show_details()

        elif choice == "5":
            update_file(customers)
            print("Logged out")
            break

        else:
            print("Invalid choice")
customers = load_customers()
while True:
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    main_choice = input("Enter choice: ")
    if main_choice == "1":
        register(customers)
    elif main_choice == "2":
        customer = login(customers)
        if customer:
            banking_menu(customer, customers)
    elif main_choice == "3":
        print("Thank you")
        break
    else:
        print("Invalid choice")