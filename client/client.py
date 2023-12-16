import sqlite3
import os
from pwinput import pwinput
from utils import valid_email
from utils import hash_password
from utils import check_password
from pathlib import Path
from utils import db_connection

DB = "secure_purchase_order.db"
PARENT_DIR = Path.cwd().parent
DB_PATH = PARENT_DIR/DB

conn = db_connection(db_path=DB_PATH)

def main():
    try:
        # User is not auth
        authenticated = False

        print("Welcome to the Secure Purchase Order client.")
        user_in = input("Are you a returning user?: (y/n): ").strip().lower()
        if user_in == 'y':
            username = input("Please enter your username: ")
            password = pwinput(prompt="Please enter your password: ")

            # Get user record by username
            cursor = conn.cursor()
            sql = "select * from users where username = ?;"
            cursor.execute(sql, (username,))
            record = cursor.fetchone()

            if record is not None:
                # Fetch columns from record, compare hash to entered pw
                id, username, email, hashed_password = record
                if check_password(password.encode(), hashed_password.encode()):
                    authenticated = True
                    print("User authenticated.")
                else:
                    print("Incorrect password, try again.")
            else:
                raise Exception("No such account with specified username.")
        elif user_in == 'n':
            username = input("Please enter a username: ")
            password = pwinput(prompt="Please enter a password: ")
            email = input("Please enter an email: ")

            if not valid_email(email):
                raise Exception("Invalid email.")
            
            # Check if this user already exists, if so throw an exception
            cursor = conn.cursor()
            sql = "select * from users where username = ? or email = ?;"
            cursor.execute(sql, (username, email))
            result = cursor.fetchall()

            if len(result) > 0:
                raise Exception("Username or email already in use.")
            
            # Insert hashed password along with other information into users
            print("Creating user account...")
            hashed_pw = hash_password(password)
            sql = "insert into users (username, email, password) values (?, ?, ?)"
            data = [username, email, hashed_pw]
            cursor.execute(sql, data)

            print("Account successfully created, please restart the client to login.")
            conn.commit()
            conn.close()
        else:
            print("Invalid selection.")
    except Exception as e:
        print(str(e))
        print("Closing program...")


if __name__ == '__main__':
    main()