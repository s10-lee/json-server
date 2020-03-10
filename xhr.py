import sys
import json
from requests import Request, Session


def pretty_print(obj, indent=0):
    if isinstance(obj, list):
        print((indent * ' ') + '[')
        for i in obj:
            pretty_print(i, indent=indent + 2)
        print((indent * ' ') + ']')
    elif isinstance(obj, dict):
        print((indent * ' ') + '{')
        for k, v in obj.items():
            if isinstance(v, int) or isinstance(v, float):
                print(((indent + 2) * ' ') + f"{k}: {v}")
            if isinstance(v, str):
                print(((indent + 2) * ' ') + f"{k}: '{v}'")
            else:
                pretty_print(v, indent=indent + 2)
        print((indent * ' ') + '}')

    else:
        if isinstance(obj, int) or isinstance(obj, float):
            obj = str(obj)
        elif isinstance(obj, str):
            obj = f"'{obj}'"
        print((2 * indent * ' ') + obj)


if __name__ == '__main__':
    method = 'GET'
    url = None
    data = None
    headers = None
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
            n = i + 1
            # print(i, a)

            if a in ['--data', '-d'] and len(sys.argv) > n:
                data = sys.argv[n]

            if a in ['--headers', '-h'] and len(sys.argv) > n:
                data = sys.argv[n]

        s = Session()
        r = Request(method, url, data=data, headers=headers).prepare()
        resp = s.send(r)

        print('*******************************************************')
        print(resp.status_code, method, resp.url)
        print('\r\n'.join([f'{k}: {v}' for k, v in resp.headers.items()]))
        # print(json.dumps(resp.json(), sort_keys=False, indent=4))
        if resp.content:
            # pretty_print(resp.json())
            print(resp.json())
        print('\r\n')
