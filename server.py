import socket
import threading


HOST = "192.168.100.193"
host = socket.gethostname()
PORT = 9010
clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

def handle_client(client_socket, client_address):
    clients.append(client_socket)
    print(f"New client connected: {client_address}")

    client_socket.send("Enter your name : ".encode("utf-8"))
    user_name = client_socket.recv(1024).decode("utf-8")
    print(f"{client_address} Clients name: {user_name}")

    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")#dekodirebis protokoli
            if msg =='exit':
                print(f"{user_name} disconnected")
                break
            if not msg:
                print(f"{user_name} disconnected.")
                break
            print(f"{user_name}:{msg}")
            broadcast(f"{user_name}:{msg}", client_socket)

        except ConnectionError as e:
            print(f"Client {user_name} disconnected")
            print(e)
            if client_socket in clients:
                clients.remove(client_socket)
            client_socket.close()
            break

    client_socket.close()

def broadcast(msg,sender_user=None):
    for client in clients:
        if client != sender_user:
            try:
                client.send(msg.encode("utf-8"))
            except:
                clients.remove(client)

def send_from_server():
    while True:
        msg = input()
        broadcast(f"SERVER: {msg}", None)

def start_server():
    print("server is running...")
    server_socket.listen()
    print("waiting for a connection")
    threading.Thread(target=send_from_server, daemon=True).start()

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

start_server()