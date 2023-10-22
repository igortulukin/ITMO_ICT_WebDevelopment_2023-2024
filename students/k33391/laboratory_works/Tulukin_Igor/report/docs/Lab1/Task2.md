# Задание 2

**Задача**: Реализовать клиентскую и серверную часть приложения. Клиент запрашивает у
сервера выполнение математической операции, параметры, которые вводятся с
клавиатуры. Сервер обрабатывает полученные данные и возвращает результат
клиенту. <br/> a. Теорема Пифагора

**Листинг кода**:<br/>

``` py title="Server.py"
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
        side = math.sqrt(sides[0]**2 + sides[1]**2)
        conn.send(bytes(str(side), 'utf-8'))
    print(data.decode("utf-8"))


conn.close()
```

``` py title="Client.py"
import socket

sock = socket.socket()
sock.connect(('localhost', 9090))
print('Enter sides')
data = input()
sock.send(bytes(data, 'utf-8'))

data = sock.recv(1024)
sock.close()

print(data.decode('utf-8'))

```

**Результат работы программы**:
![Screenshot](../img/Lab1/Task2/server.png)
![Screenshot](../img/Lab1/Task2/client.png)