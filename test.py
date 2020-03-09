from socket import *
from server import CRLF

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8888))
server.listen(5)

print('http://127.0.0.1:8888/')

while True:
    client, address = server.accept()

    rd = client.recv(5000).decode()
    print(client)
    print(rd)

    # pieces = rd.split(CRLF)
    # method, url = pieces[0].split()[0:2]

    body = ''.join([
        'HTTP/1.1 200 OK', CRLF,
        'Content-Type: application/json; charset=UTF-8', CRLF,
        'Connection: close',
        CRLF, CRLF,
        '{"some": "value"}'
    ])

    client.sendall(body.encode())
    # client.shutdown(SHUT_RDWR)
    client.close()

