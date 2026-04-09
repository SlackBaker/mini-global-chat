import socket
import threading

PORT = 5050
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}  # conn: nickname

def broadcast(msg, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(msg)
            except:
                client.close()
                clients.pop(client, None)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr}")

    # we get the nick
    nickname = conn.recv(1024).decode(FORMAT)
    clients[conn] = nickname

    broadcast(f"[SERVER] {nickname} joined".encode(FORMAT))

    while True:
        try:
            msg = conn.recv(1024).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                break

            full_msg = f"[{nickname}]: {msg}"
            print(full_msg)

            broadcast(full_msg.encode(FORMAT), conn)

        except:
            break

    # вихід
    print(f"[DISCONNECTED] {nickname}")
    broadcast(f"[SERVER] {nickname} вийшов".encode(FORMAT))

    clients.pop(conn, None)
    conn.close()

def start():
    server.listen()
    print(f"[STARTED] Server on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

print("[STARTING]")
start()
