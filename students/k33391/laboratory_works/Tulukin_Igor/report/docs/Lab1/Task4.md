# Задание 4

**Задача**: Реализовать двухпользовательский или многопользовательский чат. Реализация
многопользовательского часа позволяет получить максимальное количество
баллов.

**Листинг кода**:<br/>

``` py title="Server.py"
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
    server_address = ('', 9090)
    server = Server(server_address)
    server.run()

```

``` py title="Client.py"
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
    server_address = ('localhost', 9090)
    user = User(server_address)
    user.start()
```

**Результат работы программы**:
![Screenshot](../img/Lab1/Task4/server.png)
![Screenshot](../img/Lab1/Task4/client1.png)
![Screenshot](../img/Lab1/Task4/client2.png)