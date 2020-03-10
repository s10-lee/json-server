import sys
import json
from datetime import datetime
from socket import *

# <CR><LF> - carriage return & line feed (newline)
CRLF = '\r\n'
PACKET_SIZE = 4096
PROTOCOL = 'HTTP/1.1'
CONTENT_TYPE = 'application/json; charset=UTF-8'
HEADERS = ['Server', 'Date', 'Allow', 'Content-type', 'Connection']
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


def red(text):
    return f"\033[1;31m{text}\033[0m"


def green(text):
    return f"\033[1;32m{text}\033[0m"


def cyan(text):
    return f"\033[1;36m{text}\033[0m"


def yellow(text):
    return f"\033[1;33m{text}\033[0m"


def get_response(status=204, body=None, extra=None):
    s = sys.version_info
    dt = datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
    r = [f'{PROTOCOL} {status} {STATUSES.get(status)}']
    h = {
        'Server': f'JSON-Server, Python {s.major}.{s.minor}.{s.micro}',
        'Date': dt,
        'Content-Type': CONTENT_TYPE,
        'Connection': 'close'
    }

    if extra:
        h.update(extra)

    r += [f'{k}: {v}' for k, v in h.items()] + [CRLF]
    response = CRLF.join(r).encode()

    if body:
        if isinstance(body, dict) or isinstance(body, list):
            body = json.dumps(body)

        if isinstance(body, str):
            body = body.encode()

        response += body

    return response


def run(host, port, db_path):

    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # Database
    with open(db_path) as f:
        db = json.load(f)

    try:
        server.bind((host, int(port)))
        server.listen(5)

        # Greetings
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
                client.close()
                continue

            pieces = rd.split(CRLF)
            method, url = pieces[0].split()[0:2]
            body = None
            status_code = 200

            # Favicon
            if url == '/favicon.ico':
                with open('favicon.ico', 'rb') as fp:
                    # h = get_response(status_code, extra={'Content-type': 'image/vnd.microsoft.icon'})
                    # output = h.encode() + fp.readlines()[0]
                    output = get_response(status_code, fp.readlines()[0],
                                          {'Content-type': 'image/vnd.microsoft.icon'})

                    client.sendall(output)
                    client.close()

                print(green('/favicon.ico'))
                continue

            print(CRLF, color_text(f'************ {td} **************', 'cyan'), CRLF, rd, sep='')

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

            client.sendall(output)
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
