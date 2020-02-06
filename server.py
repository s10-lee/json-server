from socket import *
from src.console import Console


def run():
    server = socket(AF_INET, SOCK_STREAM)
    try:
        server.bind(('localhost', 8888))
        server.listen(5)

        while True:
            client, address = server.accept()

            rd = client.recv(5000).decode()
            pieces = rd.split('\r\n')

            if len(pieces):
                print(pieces)

            output = "HTTP/1.1 200 OK\r\n"
            output += "Content-Type: text/html; charset=utf-8\r\n"
            output += "\r\n<html><body><h1>Hello, World</h1></body></html>\r\n\r\n"
            client.sendall(output.encode())
            client.close()
            # client.shutdown(0)

    except KeyboardInterrupt:
        print('\nShutting down...\n')

    except Exception as e:
        print('\nError:')
        print(e)

    finally:
        server.close()


print('\nGo to http://localhost:8888\n')
run()
