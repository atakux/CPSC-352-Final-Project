import sys
import os

# Append parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import socket
import threading
from utils import db_connection
from cryptography_utils import gen_public_private_keys
from cryptography_utils import export_private_key
from cryptography_utils import export_public_key
from cryptography_utils import import_private_key
from cryptography_utils import import_public_key

SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "QUIT"

def handle_client(conn: socket.socket, addr: tuple):
    print(f"Incoming connection from: {addr}")
    
    username = conn.recv(SIZE).decode(FORMAT)
    print(f"Connected with: {username}")

    public_key_file = f"{username}_public_key.pem"
    user_public_key = import_public_key(public_key_file)

    connected = True
    while connected:
        message = conn.recv(SIZE).decode(FORMAT)

        print(f"{addr} sent: {message}")
        
        if message == DISCONNECT_MESSAGE:
            connected = False

        message = "Test"
        conn.send(message.encode(FORMAT))
    
    conn.close()

threads = []

def main():
    try:
        # Export public and private keys (private key goes into CWD)
        public_key, private_key = gen_public_private_keys()
        export_private_key(private_key, "server_private_key.pem")
        export_public_key(public_key, "../client/server_public_key.pem")

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
        print("Listening for incoming connections...")

        while True:
            conn, addr = server.accept()
            print(f"Incoming client: {addr}")
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

    except KeyboardInterrupt:
        print("Keyboard interrupt found, shutting down...")
    except Exception as e:
        print(str(e))
    finally: 
        if 'server' in locals():
            server.close()
        for thread in threads:
            thread.join()


if __name__ == '__main__':
    main()
    