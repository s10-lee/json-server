#
# HTTP 1.1 Response
#
# <CR><LF> - caret return & line feed (newline)

CRLF = '\r\n'
PROTOCOL = 'HTTP/1.1'
CONTENT_TYPE = 'application/json; charset=utf-8'
ALLOWED_METHODS = 'GET, HEAD, OPTIONS'

HEADERS = {
    'Allow': ALLOWED_METHODS,
    'Content-Type': CONTENT_TYPE
}


STATUSES = {
    200: 'OK',

    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',

    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway'
}


class Response:

    def __init__(self, status=200, body=None):
        self.status_code = status
        self.status_message = STATUSES.get(status)
        self.body = body

    def __str__(self):
        return CRLF.join([
            f'{PROTOCOL} {self.status_code} {self.status_message}',
            f'Content-type: {CONTENT_TYPE}',

            CRLF,
            self.body,
            CRLF
        ])
