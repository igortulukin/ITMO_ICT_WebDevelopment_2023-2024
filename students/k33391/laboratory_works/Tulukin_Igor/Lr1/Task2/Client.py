import socket

sock = socket.socket()
sock.connect(('localhost', 9090))
print('Enter sides')
data = input()
sock.send(bytes(data, 'utf-8'))

data = sock.recv(1024)
sock.close()

print(data.decode('utf-8'))
