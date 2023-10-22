import socket

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.connect(('localhost', 9090))
sock.send(b'Hello, Server!')

data = sock.recv(1024)
sock.close()

print(data.decode('utf-8'))
