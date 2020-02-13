#
# HTTP 1.1 Request
#

SEPARATOR = '\r\n'
METHODS = [
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]

ALLOWED_METHODS = ['GET', 'HEAD', 'OPTIONS']


class Request:

    def __init__(self, req):
        rd = req.split(SEPARATOR)

        request_method, request_url = rd.pop(0).split()[0:1]

        print('Request method:', request_method)
        print('URL:', request_url)
        print('Left:', rd)

        self.headers = []
