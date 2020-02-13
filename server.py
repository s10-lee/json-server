import sys
import json

from socket import *
from src.console import Console
from src.http import Request, Response


def run(host, port, db_path):
    server = socket(AF_INET, SOCK_STREAM)
    try:
        server.bind((host, int(port)))
        server.listen(5)

        # database file
        with open(db_path) as f:
            db = json.load(f)

        Console.write('\nWelcome to JSON Server !\n', 'green', bold=True)
        Console.write(f'http://{host}:{port}\n', 'cyan', bold=True)

        while True:
            client, address = server.accept()

            rd = client.recv(5000).decode()

            Console.write('\n*********', 'blue', bold=True)
            print(rd)

            rq = Request(rd)

            if not rq.is_implemented_method():
                rs = Response(501)

            elif not rq.is_allowed_method():
                rs = Response(405)

            else:

                body = None
                alias = rq.url.strip('/')

                for a in db:
                    if a == alias:
                        body = db[a]

                if body is None:
                    if alias:
                        rs = Response(404)
                    else:
                        rs = Response(204)
                else:
                    rs = Response(200, body)

            output = rs.get_result()
            client.sendall(output)
            client.close()
            # client.shutdown(0)

    except KeyboardInterrupt:
        Console.write('\nShutting down...\n', bold=True)

    # except Exception as e:
    #     Console.write('\nError:', 'red')
    #     Console.write(f' {e}\n', 'red', bold=True)

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
