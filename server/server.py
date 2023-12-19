import sys
import os

# Append parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import socket
import threading
from cryptography_utils import gen_public_private_keys
from cryptography_utils import export_key
from cryptography_utils import import_key
from cryptography_utils import encrypt_message
from cryptography_utils import decrypt_message
from cryptography_utils import sign_message
from cryptography_utils import verify_sign
from cryptography_utils import extract_timestamp
from cryptography_utils import verify_timestamp
from utils import place_order
from typing import List

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "QUIT"
VIEW_INV = "VIEW"
PLACE_ORDER = "ORDER"
CHANGE_PW = "PWD"

def handle_client(conn: socket.socket, addr: tuple):
    # This is where the bulk of handling responses from the client will go
    print(f"Incoming connection from: {addr}")
    print(addr)
    
    username = conn.recv(SIZE).decode(FORMAT)

    print(f"Connected with: {username}")

    server_private_key = import_key("server_private_key.pem")
    user_public_key = import_key(f"{username}_public_key.pem")        

    connected = True
    while connected:
        encrypted_message = conn.recv(SIZE)
        decrypted_message = decrypt_message(encrypted_message, server_private_key, FORMAT)
        message, time_stamp = extract_timestamp(decrypted_message)

        print(f"{addr} sent: {message} at {time_stamp}")

        if verify_timestamp(time_stamp):
            if message.upper() == DISCONNECT_MESSAGE:
                connected = False
            elif message.upper() == VIEW_INV:
                # TODO: implement this
                print("client chose to view inventory")
            elif message.upper() == PLACE_ORDER:
                # TODO: implement this
                    item_options = "Bagel, Toast, Croissant"
                    encrypted_items = encrypt_message(item_options.encode(FORMAT), user_public_key)
                    
                    signed_items = sign_message(encrypted_items, server_private_key)
                    conn.send(encrypted_items + signed_items)

                    # Receive encrypted choice & signature
                    encrypted_choice = conn.recv(SIZE)
                    usr_choice_enc = encrypted_choice[:-256]
                    signature = encrypted_choice[-256:]

                    # Verify signature
                    if verify_sign(usr_choice_enc, signature, user_public_key):

                        usr_choice = decrypt_message(usr_choice_enc, server_private_key, FORMAT)

                        print(f"{username} wants {usr_choice}")
                        
                        # Send confirmation of email to client
                        confirmation = f"Sent an order confirmation for your purchase of {usr_choice} to your email, {username}!"
                        encrypted_conf = encrypt_message(confirmation.encode(FORMAT), user_public_key)
                        conn.send(encrypted_conf)

                        place_order(username, usr_choice)
                    else:
                        print("Signature did not match.")

            elif message.upper() == CHANGE_PW:
                # TODO: implement this
                print("client chose to change password")
        else:
            print("Replayed message detected")
    
    conn.close()

# All threads
threads: List[threading.Thread] = []

def main():
    try:
        server = None

        # Export public and private keys (private key goes into CWD)
        public_key, private_key = gen_public_private_keys()
        export_key(private_key, "server_private_key.pem")
        export_key(public_key, "../client/server_public_key.pem")

        server = socket.socket()
        # Allow reuse of this socket address
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ip = input("Please input the server ip: ").strip()
        port = int(input("Please input the port to connect to: ").strip())
        addr = (ip, port)

        print(f"Server has started, listening on {ip}:{port}")
        print("Waiting for client to connect...")

        server.bind(addr)
        server.listen()
        print(f"Listening for incoming connections... on {ip}:{port}")

        while True:
            conn, addr = server.accept()
            print(f"Incoming client: {addr}")
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

            # Append all threads to the threads list to later call join()
            threads.append(thread)
    except KeyboardInterrupt:
        print("Keyboard interrupt found (CTRL+C), shutting down...")
    except Exception as e:
        print(str(e))
    finally:
        # If server exists, close it
        if server:
            server.close()
        
        # Clean up threads by calling join()
        for thread in threads:
            if thread.is_alive():
                thread.join()


if __name__ == '__main__':
    main()