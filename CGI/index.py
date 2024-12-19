import codecs
import json
import os
import sys
import urllib.parse
from cgi import FieldStorage

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

def send_error(code: int = 400, phrase: str = "Bad Request", explain: str = None):
    print(f"Status: {code} {phrase}")
    print("Content-Type: text/plain; charset=utf-8")
    print()
    print(explain if explain else phrase, end='')
    exit()

envs = {k: v for k, v in os.environ.items() if k in ('REQUEST_METHOD', 'QUERY_STRING', 'REQUEST_URI')}
headers = {
    (k[5:] if k.startswith('HTTP_') else k).lower().replace("_", "-"): v
    for k, v in os.environ.items()
    if k.startswith('HTTP_') or k in ('CONTENT_TYPE', 'CONTENT_LENGTH')
}

query_string = urllib.parse.unquote(envs.get('QUERY_STRING', ''), encoding="utf-8")
query_parameters = dict(pair.split('=', maxsplit=1) if '=' in pair else (pair, None)
                        for pair in query_string.split('&') if pair != "")

body_parameters = {}
body = sys.stdin.read()
if body:
    if headers.get('content-type') == 'application/json': body_parameters = json.loads(body)
    elif headers.get('content-type') == 'application/x-www-form-urlencoded':
        body_parameters = dict(
            pair.split('=', maxsplit=1)
            for pair in urllib.parse.unquote(body).split('&') if '=' in pair
        )
    elif headers.get('content-type', '').startswith('multipart/form-data'):
        form = FieldStorage()
        body_parameters = {field: form[field].value for field in form.keys()}
    else: send_error(415, "Unsupported Media Type", "Supported MIME types: application/json, application/x-www-form-urlencoded, multipart/form-data")

response = {
    "status_code": 200,
    "method": envs.get('REQUEST_METHOD'),
    "query_parameters": query_parameters,
    "headers": headers,
    "body_parameters": body_parameters
}

print("Content-Type: application/json; charset=utf-8")
print()
print(json.dumps(response, ensure_ascii=False), end="")