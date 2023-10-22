import socket

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(('', 9090))

while True:
    data = sock.recvfrom(1024)
    if not data:
        break
    print(data[0].decode("utf-8"))
    sock.sendto(b'Hello, Client!', data[1])
    break
