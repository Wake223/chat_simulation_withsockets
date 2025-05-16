import socket
import threading

HOST = "192.168.100.193"

PORT = 9010

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

msg = client_socket.recv(1024).decode('UTF-8')
print(msg)

def message_receiver():
    while True:
        try:
            msg1 = client_socket.recv(1024).decode('UTF-8')
            if not msg1:
                print("Server disconnected.")
                break
            print(msg1)
        except:
                print("Connection lost.")
                break
def send_message():
    while True:
        msg_send = input()
        client_socket.send(msg_send.encode('UTF-8'))

        if msg_send.lower() == "exit":
            client_socket.close()
            break
threading.Thread(target=message_receiver, daemon=True).start()
threading.Thread(target=send_message).start()