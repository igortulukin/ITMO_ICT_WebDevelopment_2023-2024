import socket
import threading



class User:
    def __init__(self, address):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address

    def start(self):
        self.client.connect(self.address)
        server_message = self.client.recv(1024).decode('utf-8')
        print(server_message)
        message = input()
        self.client.send(message.encode('UTF-8'))
        threading.Thread(target=self.receive_message).start()
        threading.Thread(target=self.send_message()).start()

    def receive_message(self):
        while True:
            message = self.client.recv(4096).decode('UTF-8')
            print(message)

    def send_message(self):
        while True:
            message = input()
            self.client.send(message.encode('UTF-8'))


if __name__ == "__main__":
    server_address = ('localhost', 8080)
    user = User(server_address)
    user.start()