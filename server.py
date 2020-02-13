import sys

from socket import *
from src.console import Console
from src.router import Router


def run(host, port, db_path):
    server = socket(AF_INET, SOCK_STREAM)
    try:
        server.bind((host, int(port)))
        server.listen(5)

        router = Router(db_path)

        Console.write('\nWelcome to JSON Server !\n', 'green', bold=True)
        Console.write(f'http://{host}:{port}\n', 'cyan', bold=True)

        while True:
            client, address = server.accept()

            rd = client.recv(5000).decode()
            pieces = rd.split('\r\n')

            current_url = '/'

            for p in pieces:
                if p.startswith('GET'):
                    current_url = p.split()[1].strip('/')

            content = router.get_response(current_url)

            if len(pieces):
                print('\n', pieces, '\n')

            output = "HTTP/1.1 200 OK\r\n"
            output += "Content-Type: application/json; charset=utf-8\r\n\r\n"
            output += f'{list(content)}\r\n\r\n'
            client.sendall(output.encode())
            client.close()
            # client.shutdown(0)

    except KeyboardInterrupt:
        Console.write('\nShutting down...\n', bold=True)

    except Exception as e:
        Console.write('\nError:', 'red')
        Console.write(f' {e}\n', 'red', bold=True)

    finally:
        server.close()


server_host = 'localhost'
server_port = 8888
server_db_path = 'db.json'

if len(sys.argv) > 1:
    for index, argument in enumerate(sys.argv):

        # Find port number in arguments
        if argument in ['-p', '--port'] and len(sys.argv) > index + 1:
            server_port = sys.argv[index + 1]

        if argument in ['-h', '--host'] and len(sys.argv) > index + 1:
            server_host = sys.argv[index + 1]

        if argument in ['-d', '--database'] and len(sys.argv) > index + 1:
            server_db_path = sys.argv[index + 1]

run(host=server_host, port=server_port, db_path=server_db_path)
