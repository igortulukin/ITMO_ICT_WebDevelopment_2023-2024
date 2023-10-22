import socket
import threading


class Server:
    def __init__(self, address):
        self.users = {}
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.bind(address)
        self.conn.listen(10)

    def run(self):
        while True:
            sock, addrs = self.conn.accept()
            sock.sendall('Enter your name:'.encode('UTF-8'))
            name = sock.recv(4096).decode('utf-8')
            print(sock)
            self.users[sock] = name
            self.dispatch(sock, f"{name} joined the chat!", sender=False)
            threading.Thread(target=self.wait_for_message, args=(sock,)).start()

    def dispatch(self, sender_socket, message, sender=True):
        name = self.users[sender_socket]
        for user in self.users:
            if user != sender_socket:
                if sender:
                    user.sendall(f"{name} : {message}".encode('UTF-8'))
                else:
                    user.sendall(f"{message}".encode('UTF-8'))

    def wait_for_message(self, sender_socket):
        while True:
            message = sender_socket.recv(4096).decode('utf-8')
            self.dispatch(sender_socket, message)


if __name__ == "__main__":
    server_address = ('', 8080)
    server = Server(server_address)
    server.run()
