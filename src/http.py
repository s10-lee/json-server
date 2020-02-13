#
# HTTP/1.1
#
# <CR><LF> - caret return & line feed (newline)
import json
from src.console import Console


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


class Router:

    def __init__(self, db_file):
        try:
            with open(db_file) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            Console.write(f'{db_file} not found !', 'red', bold=True)

    def fetch_data(self, url):
        url = url.split('/')
        alias = url[0]
        result = []

        # print('Alias: ', alias)
        # print('ID: ', id)

        for a in self.data:
            if a == alias:
                result = self.data[a]

        if len(url) == 2:
            filtered = filter(lambda x: str(x['id']) == url[1],  result)
            return filtered

        return result


class Request:

    def __init__(self, req):
        rd = req.split(CRLF)

        print(rd)

        rl = rd.pop(0).split()

        self.method = rl[0]
        self.url = rl[1]
        self.headers = rd

    def is_implemented_method(self):
        return self.method.upper() in METHODS

    def is_allowed_method(self):
        return self.method.upper() in ALLOWED_METHODS


class Response:

    def __init__(self, status=204, body=None):
        self.status_code = status
        self.status_message = STATUSES.get(status)
        self.body = body

        self.data = [
            f'{PROTOCOL} {self.status_code} {self.status_message}',
            CRLF
        ]

        if body:
            self.data += [
                f'Content-Type: {CONTENT_TYPE}',
                CRLF * 2,
                str(body),
                CRLF * 2
            ]

    def get_result(self):
        return ''.join(self.data).encode()

    def __str__(self):
        return self.get_result()
