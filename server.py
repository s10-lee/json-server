import sys
import json
from datetime import datetime
from socket import *
from src.db import Database
from src.settings import CRLF, PROTOCOL, CONTENT_TYPE, STATUSES, PACKET_SIZE, ALLOWED_METHODS, METHODS
from src.console import color_text, green, yellow, cyan


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

    database = Database(db_path)
    # database.save()

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

                # Search by route_name and primary_key
                body = database.select(alias, pk)

                if method == 'POST':
                    # todo: create new entry in db.json
                    print('Method POST')
                elif method == 'PUT':
                    # todo: update entry
                    print('Method PUT')

                print(body)

                # Filter result by primary key - object.id
                # if body and pk:
                #     for item in body:
                #         if str(item.get('id')) == pk:
                #             body = item
                #             break
                #     else:
                #         body = None

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
