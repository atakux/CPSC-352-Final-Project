import sqlite3
import os
from pwinput import pwinput
from utils import valid_email
from pathlib import Path
from utils import db_connection

DB = "secure_purchase_order.db"
PARENT_DIR = Path.cwd().parent
DB_PATH = PARENT_DIR/DB

conn = db_connection(db_path=DB_PATH)

def main():
    try:
        print("Welcome to the Secure Purchase Order client.")
        user_in = input("Are you a returning user?: (y/n): ").strip().lower()
        if user_in == 'y':
            pass
        if user_in == 'n':
            user_name = input("Please enter a username: ")
            password = pwinput(prompt="Please enter a password: ")
            email = input("Please enter an email: ")

            if not valid_email(email):
                raise Exception("Invalid email.")
            
            
    except Exception as e:
        print(str(e))
        print("Closing program...")


if __name__ == '__main__':
    main()