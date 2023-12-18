import sys
import os

# Append parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import socket
from pathlib import Path
from pwinput import pwinput
from utils import valid_email
from utils import db_connection
from cryptography_utils import hash_password
from cryptography_utils import check_password
from cryptography_utils import gen_public_private_keys
from cryptography_utils import export_key
from cryptography_utils import import_key
from cryptography_utils import decrypt_message
from cryptography_utils import encrypt_message

DB = "secure_purchase_order.db"
PARENT_DIR = Path.cwd().parent
DB_PATH = PARENT_DIR/DB
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "QUIT"
VIEW_INV = "VIEW"
PLACE_ORDER = "ORDER"
CHANGE_PW = "PWD"

def main():
    try:
        conn = db_connection(db_path=DB_PATH)

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

            # Generate public, private key pair for this user
            public_key, private_key = gen_public_private_keys()
            user_private_key_file = f"{username}_private_key.pem"
            user_public_key_file = f"../server/{username}_public_key.pem"
            export_key(private_key, user_private_key_file)
            export_key(public_key, user_public_key_file)

            hashed_pw = hash_password(password)
            sql = "insert into users (username, email, password) values (?, ?, ?)"
            data = [username, email, hashed_pw]
            cursor.execute(sql, data)

            print("Account successfully created, please restart the client to login.")
            conn.commit()
            conn.close()
        else:
            print("Invalid selection.")

        if authenticated:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip = input("Please input the server ip: ").strip()
            port = int(input("Please input the port to connect to: ").strip())
            addr = (ip, port)
            
            user_private_key = import_key(f"{username}_private_key.pem")
            server_public_key = import_key("server_public_key.pem")

            client.connect(addr)
            print(f"Client connected to server at {ip}:{port}")

            message = f"{username}, {email}"
            client.send(message.encode(FORMAT))

            connected = True
            while connected:
                print("")

                # This is where the bulk of handling responses from server will go
                print("Please enter one of the commands below:")
                print("\t- VIEW  : View store inventory")
                print("\t- ORDER : Place an order")
                print("\t- PWD   : Change password") 
                print("\t- QUIT  : Quit the program\n")
                message = input(" > ")

                # Encrypt message to server using its public key
                encrypted_message = encrypt_message(message.encode(FORMAT), server_public_key)
                client.send(encrypted_message)

                if message.upper() == DISCONNECT_MESSAGE:
                    connected = False
                elif message.upper() == PLACE_ORDER:
                    # Receive the choices provided by the server
                    encrypted_items = client.recv(SIZE)
                    item_options = decrypt_message(encrypted_items, user_private_key, FORMAT)

                    lst_items = item_options.split(", ")

                    print("Please choose from the following options:\n")

                    # Display the choices aesthetically for the client & receive their choice
                    for i in range(len(lst_items)):
                        print(f"\t{i+1}. {lst_items[i]}")

                    item_choice = int(input(" > "))

                    # Store the item they wanted & send it back to the server
                    for i in range(len(lst_items)):
                        if item_choice == i+1:
                            usr_choice = lst_items[i]

                    encrypted_choice = encrypt_message(usr_choice.encode(FORMAT), server_public_key)
                    client.send(encrypted_choice)
                else:
                    print("Invalid selection.")
            
                # Received encrypted message from server, decrypt using our private key
                encrypted_message = client.recv(SIZE)
                decrypted_message = decrypt_message(encrypted_message, user_private_key, FORMAT)
                print(f"Received message from server: {decrypted_message}")

            client.close()
    except Exception as e:
        print(str(e))
        print("Closing program...")


if __name__ == '__main__':
    main()