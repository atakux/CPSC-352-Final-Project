import socket

def main():
    s = socket.socket()
    HOST = "127.0.0.1"
    PORT = 50000

    print("Server has started")
    print("Waiting for client to connect...")

    s.bind((HOST, PORT))
    s.listen(1)

    conn, addr = s.accept()
    print(f"Connection from {addr}")

    while True:
        msg = conn.recv(1024).decode('utf-8')
        if not msg:
            break
        print(f"{addr} sent: {msg}")
    conn.close()

if __name__ == '__main__':
    main()
    