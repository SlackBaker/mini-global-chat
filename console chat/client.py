import socket
import threading

PORT = 5050
SERVER = "IP of your server"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            print("\n" + msg)
        except:
            break

def send():
    while True:
        message = input("You: ")

        if message == DISCONNECT_MESSAGE:
            client.close()
            break

        client.send(message.encode(FORMAT))

threading.Thread(target=receive).start()
threading.Thread(target=send).start()