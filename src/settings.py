# <CR><LF> - carriage return & line feed (newline)
CRLF = '\r\n'

# Packet size
PACKET_SIZE = 4096

# Server defaults
SERVER_HOST = 'localhost'
SERVER_PORT = 8888
DB_PATH = 'db.json'

# HTTP settings
PROTOCOL = 'HTTP/1.1'
CONTENT_TYPE = 'application/json'
HEADERS = ['Server', 'Date', 'Allow', 'Content-type', 'Connection']
ALLOWED_METHODS = ['GET', 'HEAD', 'OPTIONS', 'POST']
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

# Terminal colors
# todo move to console.py
SCHEMA = {
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'purple': '35',
    'cyan': '36',
    'gray': '37'
}
