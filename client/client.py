import sqlite3
import os
from pwinput import pwinput
from utils import valid_email
from pathlib import Path
from utils import db_connection, hash_password

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
            username = input("Please enter a username: ")
            password = pwinput(prompt="Please enter a password: ")
            email = input("Please enter an email: ")

            if not valid_email(email):
                raise Exception("Invalid email.")
            
            hashed_pw = hash_password(password)
            
            cursor = conn.cursor()
            sql = "select * from users where username = ? or email = ?;"
            cursor.execute(sql, (username, email, hashed_pw[1], hashed_pw[0]))
            result = cursor.fetchall()
            
            if len(result) > 0:
                raise Exception("Username or email already in use.")

    except Exception as e:
        print(str(e))
        print("Closing program...")


if __name__ == '__main__':
    main()