import sys
# import json
from requests import Request, Session
from server import color_text, STATUSES, CONTENT_TYPE, CRLF

if __name__ == '__main__':
    method = 'GET'
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
            # print(i, a)

            if a in ['--data', '-d'] and len(args) >= i + 1:
                data = args[i + 1].encode('utf-8')

            if a in ['--headers', '-h'] and len(args) >= i + 1:
                headers = args[i + 1]

        s = Session()
        r = Request(method, url, data=data, headers=headers).prepare()
        resp = s.send(r)

        print(method.upper(), color_text(resp.url, 'cyan'))

        code = resp.status_code
        code_color = 'green'
        if code >= 400:
            code_color = 'yellow'
        if code >= 500:
            code_color = 'red'

        print(color_text(f'{code} {STATUSES.get(code)}', code_color))
        print(CRLF.join([f'{k}: {v}' for k, v in resp.headers.items()]))
        if resp.content:
            print(CRLF, resp.json(), sep='')
        print(CRLF)
