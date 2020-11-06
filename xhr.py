#
# Making HTTP requests from terminal.
# Simple curl wrapper.
#
#   COMMAND:
#       > python3 xhr.py [METHOD:GET] URL [OPTIONS]
#
#   METHOD:
#       GET, HEAD, POST, etc. Case insensitive. Can be omitted. GET by default.
#
#   URL:
#       Protocol and port can be omitted.
#       [PROTOCOL]HOST[:PORT]/path/to/whatever/
#
#   OPTIONS:
#       --data, -d      JSON Data                       None
#       --headers, -h   Additional HTTP headers         {'Content-type': 'application/json; charset=UTF-8'}
#       --verbose, -v   Show response headers           None
#
#   USAGE:
#
#       > python3 xhr.py POST http://127.0.0.1/your/url/ --data "{'name': 'John'}"
#       > python3 xhr.py localhost:8888 -h '{"Cache-control": "no-cache"}"
#
#       Known issue - troubles with single / double quotes
#
#   TIP:
#       Add alias to bash_profile
#       alias xhr="/path/to/python3 /path/to/xhr.py"
#


import sys
import json
from requests import Request, Session
from server import STATUSES, CONTENT_TYPE, CRLF
from src.console import print_line


if __name__ == '__main__':
    method = 'GET'
    verbose = False
    url = None
    data = None
    headers = {'Content-type': CONTENT_TYPE}
    args = sys.argv[1:]
    if len(sys.argv) > 0:
        first = args.pop(0)
        if first.upper() in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            method = first
            url = args.pop(0)
        else:
            url = first

        if not url.startswith('http'):
            url = 'http://' + url

        for i, a in enumerate(args):

            if a in ['--data', '-d'] and len(args) >= i + 1:
                data = args[i + 1].encode('utf-8')

            if a in ['--headers', '-h'] and len(args) >= i + 1:
                headers = json.loads(args[i + 1])

            if a in ['-v']:
                verbose = True

        s = Session()
        r = Request(method, url, data=data, headers=headers).prepare()
        resp = s.send(r)

        code = resp.status_code
        color = 'green'
        if code >= 400:
            color = 'yellow'
        if code >= 500:
            color = 'red'

        if verbose:
            print_line(f'<{color}>{code} {STATUSES.get(code)}</{color}>')
            print(CRLF.join([f'{k}: {v}' for k, v in resp.headers.items()]))

        if resp.content:
            if resp.json():
                print(CRLF, resp.json(), sep='')
            else:
                print(CRLF, resp.content, sep='')
        print_line('<nl>')
