import math
import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(10)
conn, addr = sock.accept()

print('connected:', addr)

while True:
    data = conn.recv(16384)
    if not data:
        break
    sides = [int(x) for x in data.split()]
    if len(sides) != 2:
        conn.send(b'Wrong number of sides')
    else:
        side = math.sqrt(sides[0] ** 2 + sides[1] ** 2)
        conn.send(bytes(str(side), 'utf-8'))
    print(data.decode("utf-8"))

conn.close()
