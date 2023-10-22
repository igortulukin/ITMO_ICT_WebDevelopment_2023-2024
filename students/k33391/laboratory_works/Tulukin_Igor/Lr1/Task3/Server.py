import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 9090))
sock.listen(10)

while True:
    connection, address = sock.accept()
    data = connection.recv(16384)
    header = 'HTTP/1.1 200 OK\n'
    mimetype = 'text/html'
    header += 'Content-Type: ' + str(mimetype) + '\n\n'
    file = open('page.html', 'rb')
    response = file.read()
    file.close()
    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
