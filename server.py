import sys
from socket import *
from src.console import Console


def run(host='localhost', port=8888):
    server = socket(AF_INET, SOCK_STREAM)
    try:
        server.bind((host, int(port)))
        server.listen(5)

        Console.write('\nWelcome to JSON Server !', 'green', True)
        Console.write('Go to:')
        Console.write(f'http://{host}:{port}\n', 'cyan', bold=True)

        while True:
            client, address = server.accept()

            rd = client.recv(5000).decode()
            pieces = rd.split('\r\n')

            if len(pieces):
                print('\n', pieces, '\n')

            output = "HTTP/1.1 200 OK\r\n"
            output += "Content-Type: application/json; charset=utf-8\r\n"
            output += '\r\n{"some": "one", "two": 22, "boolean": false}\r\n\r\n'
            client.sendall(output.encode())
            client.close()
            # client.shutdown(0)

    except KeyboardInterrupt:
        Console.write('\nShutting down...\n', 'gray', True)

    except Exception as e:
        Console.write('\nError:', 'red', True)
        Console.write(f' - {e}\n', 'red')

    finally:
        server.close()


server_host = 'localhost'
server_port = 8888
if len(sys.argv) > 1:
    for index, argument in enumerate(sys.argv):

        # Find port number in arguments
        if argument in ['-p', '--port'] and len(sys.argv) > index + 1:
            server_port = sys.argv[index + 1]

        if argument in ['-h', '--host'] and len(sys.argv) > index + 1:
            server_host = sys.argv[index + 1]

run(host=server_host, port=server_port)
