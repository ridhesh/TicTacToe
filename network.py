# network.py
import socket
import threading

class Network:
    def __init__(self):
        self.server = None
        self.clients = []

    def start_server(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        print(f"Server started on {host}:{port}")

        while True:
            client, address = self.server.accept()
            print(f"Connection from {address} has been established.")
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            try:
                msg = client.recv(1024).decode()
                if msg:
                    self.broadcast(msg, client)
                else:
                    break
            except:
                break

    def broadcast(self, msg, client):
        for c in self.clients:
            if c != client:
                c.send(msg.encode())
