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
        
        username = conn.recv(SIZE).decode(FORMAT)
        print(f"Connected with: {username}")

        server_private_key = import_key("server_private_key.pem")
        user_public_key = import_key(f"{username}_public_key.pem")        

        connected = True
        while connected:
            encrypted_message = conn.recv(SIZE)
            decrypted_message = decrypt_message(encrypted_message, server_private_key, FORMAT)

            print(f"{addr} sent: {decrypted_message}")
            
            if decrypted_message.upper() == DISCONNECT_MESSAGE:
                connected = False
            elif decrypted_message.upper() == VIEW_INV:
                # TODO: implement this
                print("client chose to view inventory")
            elif decrypted_message.upper() == PLACE_ORDER:
                # TODO: implement this
                print("client chose to place order")
            elif decrypted_message.upper() == CHANGE_PW:
                # TODO: implement this
                print("client chose to change password")

            message = "Test"
            encrypted_message = encrypt_message(message.encode(FORMAT), user_public_key)
            conn.send(encrypted_message)
        
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
    