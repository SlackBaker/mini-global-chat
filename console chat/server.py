import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")
    clients.append(conn)

    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break

            decoded = msg.decode(FORMAT)

            if decoded == DISCONNECT_MESSAGE:
                break

            print(f"[{addr}] {decoded}")
            broadcast(msg, conn)

        except:
            break

    clients.remove(conn)
    conn.close()
    print(f"[DISCONNECTED] {addr}")

def start():
    server.listen()


    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

print("[STARTING]")
start()