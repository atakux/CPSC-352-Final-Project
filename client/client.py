import sqlite3
import os
from pwinput import pwinput
from utils import valid_email
path = os.getcwd()

def main():
    try:
        print("Welcome to the Secure Purchase Order client.")
        user_in = input("Are you a returning user?: (y/n): ").strip().lower()
        if user_in == 'y':
            pass
        if user_in == 'n':
            user_name = input("Please enter a username: ")
            email = input("Please enter an email: ")

            if not valid_email(email):
                raise Exception("Invalid email.")
        


            user_pass = pwinput(prompt="Please enter a password: ")
    except Exception as e:
        print(str(e))
        print("Closing program...")


if __name__ == '__main__':
    main()