import sys
import json
from datetime import datetime

from socket import *

# <CR><LF> - carriage return & line feed (newline)
CRLF = '\r\n'
PACKET_SIZE = 1024
PROTOCOL = 'HTTP/1.1'
CONTENT_TYPE = 'application/json; charset=UTF-8'
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

# test commit

SCHEMA = {
    # 'white': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'purple': '35',
    'cyan': '36',
    'gray': '37'
}


def color_text(text, color, bold=True):
    return f"\033[{int(bold)};{SCHEMA.get(color, '37')}m{text}\033[0m"


def get_response(status=204, body=None):
    s = sys.version_info
    dt = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    response = CRLF.join([f'{PROTOCOL} {status} {STATUSES.get(status)}',
                          f'Server: JSON-Server, Python {s.major}.{s.minor}.{s.micro}',
                          f'Date: {dt}',
                          f'Content-Type: {CONTENT_TYPE}',
                          'Content-Language: en',
                          'Access-Control-Allow-Origin: *',
                          'Connection: close']) + CRLF
    if body:
        response += f'{CRLF}{json.dumps(body)}'

    # print(color_text('Response:', 'gray'))
    # print(response, CRLF, sep='')

    return response


def run(host, port, db_path):
    server = socket(AF_INET, SOCK_STREAM)

    # database file
    with open(db_path) as f:
        db = json.load(f)

    try:
        server.bind((host, int(port)))
        server.listen(5)

        # Say hello to terminal
        print('\n\n', color_text('Welcome to JSON Server !', 'green'),
              '\n\n', color_text(f'http://{host}:{port}', 'cyan'),
              '\n\n')

        while True:
            client, address = server.accept()

            # rd = ''
            # while True:
            #     data = client.recv(PACKET_SIZE)
            #     if not data:
            #         break
            #     rd += data.decode()

            td = datetime.now().strftime('%H:%M:%S')
            rd = client.recv(5000).decode()
            pieces = rd.split(CRLF)

            print(CRLF, color_text(f'************ {td} **************', 'cyan'),
                  CRLF, 'Address: ', address,
                  CRLF, color_text('>>>', 'cyan'),
                  CRLF, rd, sep='')

            if len(pieces) < 2:
                print('EMPTY request data!', CRLF * 2, sep='')
                continue

            method, url = pieces[0].split()[0:2]
            body = None

            # Request info
            # print(CRLF * 2, color_text(method, 'gray'),
            #       CRLF, color_text(url, 'cyan'),
            #       CRLF, pieces[1:],
            #       CRLF * 2, sep='')

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
            # client.shutdown(SHUT_RDWR)
            client.close()

    except KeyboardInterrupt:
        # TODO: How to client.shutdown(SHUT_RDWR) ?
        print(CRLF)
        print(color_text('Shutting down...', 'gray'))
        print(CRLF)

    finally:
        # print('Finally')
        # server.shutdown(SHUT_RDWR)
        server.close()


if __name__ == '__main__':
    server_host = 'localhost'
    server_port = 8888
    server_db_path = 'db.json'

    if len(sys.argv) > 1:
        for index, argument in enumerate(sys.argv):

            # Find port number in arguments
            if argument in ['--port', '-p'] and len(sys.argv) > index + 1:
                server_port = sys.argv[index + 1]

            if argument in ['--host'] and len(sys.argv) > index + 1:
                server_host = sys.argv[index + 1]

            if argument in ['--data', '-d'] and len(sys.argv) > index + 1:
                server_db_path = sys.argv[index + 1]

    run(host=server_host, port=server_port, db_path=server_db_path)
