import socket

SIZE = 1024
FORMAT = "utf-8"

def main():
    server = socket.socket()
    ip = input("Please input the server ip: ").strip()
    port = int(input("Please input the port to connect to: ").strip())
    addr = (ip, port)

    print(f"Server has started, listening on {ip}:{port}")
    print("Waiting for client to connect...")

    server.bind(addr)
    server.listen()

    conn, addr = server.accept()
    print(f"Accepted connection from: {addr}")

    while True:
        msg = conn.recv(SIZE).decode(FORMAT)
        
        if msg == 'QUIT':
            break
        
        print(f"{addr} sent: {msg}")
        
    conn.close()

if __name__ == '__main__':
    main()
    