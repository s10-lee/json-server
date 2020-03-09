import sys
import json
from datetime import datetime

from socket import *

# <CR><LF> - carriage return & line feed (newline)
CRLF = '\r\n'
PACKET_SIZE = 4096
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


def green(text):
    return f"\033[1;32m{text}\033[0m"


def cyan(text):
    return f"\033[1;36m{text}\033[0m"


def yellow(text):
    return f"\033[1;33m{text}\033[0m"


def get_response(status=204, body=None, extra_headers=None):
    s = sys.version_info
    dt = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    start_line = f'{PROTOCOL} {status} {STATUSES.get(status)}'
    headers = {
        'Server': f'JSON-Server, Python {s.major}.{s.minor}.{s.micro}',
        'Date': dt,
        'Content-Type': CONTENT_TYPE,
        'Connection': 'close'
    }

    if extra_headers:
        for k, v in extra_headers.items():
            headers[k] = v

    lines = [start_line] + [f'{k}: {v}' for k, v in headers.items()] + [CRLF]
    response = CRLF.join(lines)

    if body:
        response += json.dumps(body)

    return response


def run(host, port, db_path):

    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # database file
    with open(db_path) as f:
        db = json.load(f)

    try:
        server.bind((host, int(port)))
        server.listen(5)

        # Greetings !
        print(CRLF, green('Welcome to JSON Server !'), cyan(f'http://{host}:{port}'), sep=CRLF * 2)

        while True:
            headers = {}
            client, address = server.accept()

            # todo: Work around timeout
            # client.settimeout(60)
            # except socket.timeout

            td = datetime.now().strftime('%H:%M:%S')
            rd = client.recv(PACKET_SIZE).decode()

            # Check received data
            if not rd:
                print(yellow('EMPTY !'), CRLF * 2, sep='')
                continue

            print(CRLF, color_text(f'************ {td} **************', 'cyan'), CRLF, rd, sep='')
            pieces = rd.split(CRLF)
            # if len(pieces) < 2:
            #     print('EMPTY request data!', CRLF * 2, sep='')
            #     continue

            method, url = pieces[0].split()[0:2]
            body = None
            status_code = 200

            # Favicon
            # todo: get_response() should be using instead
            if url == '/favicon.ico':
                with open('favicon.ico', 'rb') as fp:
                    [ico] = fp.readlines()
                    # Mime image/x-icon
                    headers = CRLF.join([f'{PROTOCOL} 200 OK', 'Content-type: image/vnd.microsoft.icon']) + CRLF * 2
                    output = headers.encode() + ico
                    client.sendall(output)

                print(green('Favicon OK'))
                continue

            if method not in METHODS:
                status_code = 501
            elif method not in ALLOWED_METHODS:
                status_code = 405
                headers['Allow'] = ', '.join(ALLOWED_METHODS)
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

            output = get_response(status_code, body, headers)

            client.sendall(output.encode())
            client.shutdown(SHUT_RDWR)
            client.close()

    except KeyboardInterrupt:
        print(CRLF)
        print(color_text('Shutting down...', 'gray'))
        print(CRLF)

    finally:
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

            if argument in ['--host', '-h'] and len(sys.argv) > index + 1:
                server_host = sys.argv[index + 1]

            if argument in ['--data', '-d'] and len(sys.argv) > index + 1:
                server_db_path = sys.argv[index + 1]

    run(host=server_host, port=server_port, db_path=server_db_path)
