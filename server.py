import sys
import json

from socket import *
from src.console import Console

# <CR><LF> - caret return & line feed (newline)
CRLF = '\r\n'
PROTOCOL = 'HTTP/1.1'
CONTENT_TYPE = 'application/json; charset=utf-8'
ALLOWED_METHODS = ['GET', 'HEAD', 'OPTIONS']
METHODS = ['GET', 'HEAD', 'POST', 'DELETE', 'OPTIONS']
STATUSES = {
    200: 'OK',
    201: 'Created',
    204: 'No Content',

    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',

    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway'
}


def get_response(status=204, body=None):
    if body:
        data = [
            f'{PROTOCOL} {status} {STATUSES.get(status)}',
            CRLF,
            f'Content-Type: {CONTENT_TYPE}',
            CRLF * 2,
            str(body),
            CRLF * 2
        ]
    else:
        data = [
            f'HTTP/1.1 {status} {STATUSES.get(status)}',
            CRLF,
            f'Content-Type: {CONTENT_TYPE}',
            CRLF,
        ]
    return ''.join(data)



def run(host, port, db_path):
    server = socket(AF_INET, SOCK_STREAM)

    # database file
    with open(db_path) as f:
        db = json.load(f)

    try:
        server.bind((host, int(port)))
        server.listen(5)

        Console.write('\nWelcome to JSON Server !\n', 'green', bold=True)
        Console.write(f'http://{host}:{port}\n', 'cyan', bold=True)

        while True:
            client, address = server.accept()

            rd = client.recv(5000).decode()
            pieces = rd.split(CRLF)

            if not len(pieces):
                print('EMPTY request data!', '\n')
                break

            method, url = pieces[0].split()[0:2]
            body = None

            if method not in METHODS:
                status_code = 501
            elif method not in ALLOWED_METHODS:
                status_code = 405
            else:
                parts = url.strip('/').split('/')
                pk = None
                if len(parts) > 1:
                    pk = parts[-1]
                    alias = '/'.join(parts[0:-1])
                else:
                    alias = parts[0]

                # Filter result by route
                for a in db:
                    if a == alias:
                        body = db[a]
                        break

                # Filter result by primary key - object.id
                if body and pk:
                    for item in body:
                        if str(item.get('id')) == pk:
                            body = item
                            break
                    else:
                        body = None

                if not body:
                    status_code = 404
                else:
                    status_code = 200

            output = get_response(status_code, body)

            client.sendall(output.encode())
            client.close()
            # client.shutdown(0)

    except KeyboardInterrupt:
        Console.write('\nShutting down...\n', bold=True)

    # except Exception as e:
    #     Console.write('\nError:', 'red')
    #     Console.write(f' {e}\n', 'red', bold=True)

    finally:
        server.close()


if __name__ == '__main__':
    server_host = 'localhost'
    server_port = 8888
    server_db_path = 'db.json'

    if len(sys.argv) > 1:
        for index, argument in enumerate(sys.argv):

            # Find port number in arguments
            if argument in ['--port'] and len(sys.argv) > index + 1:
                server_port = sys.argv[index + 1]

            if argument in ['--host'] and len(sys.argv) > index + 1:
                server_host = sys.argv[index + 1]

            if argument in ['--data'] and len(sys.argv) > index + 1:
                server_db_path = sys.argv[index + 1]

    run(host=server_host, port=server_port, db_path=server_db_path)
