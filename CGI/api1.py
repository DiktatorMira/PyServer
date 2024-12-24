#!C:/Python313/python.exe
import codecs
import json
import os
import sys
import urllib.parse

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

def send_error(code=400, phrase="Bad Request", explain=None):
    print(f"Status: {code} {phrase}")
    print("Content-Type: text/plain; charset=utf-8")
    print()
    print(explain if explain else phrase)
    exit()

def parse_multipart_form_data(body, content_type):
    """Parses multipart/form-data."""
    boundary = "--" + content_type.split("boundary=")[1]
    parts = body.split(boundary)
    parts = parts[1:-1]  # Remove preamble and epilogue
    parsed_data = {}

    for part in parts:
        if not part.strip(): continue
        headers, content = part.split("\r\n\r\n", maxsplit=1)
        content = content.rstrip("\r\n")  # Remove trailing newlines

        headers_dict = {}
        for header_line in headers.split("\r\n"):
            if ": " in header_line:
                key, value = header_line.split(": ", maxsplit=1)
                headers_dict[key.lower()] = value

        disposition = headers_dict.get("content-disposition", "")
        if "name=" in disposition:
            field_name = disposition.split("name=")[1].split(";")[0].strip('"')
            parsed_data[field_name] = content
    return parsed_data

envs = {
    k: v for k, v in os.environ.items()
    if k in ('REQUEST_METHOD', 'QUERY_STRING', 'REQUEST_URI')
}
headers = {
    (k[5:] if k.startswith('HTTP_') else k).lower().replace("_", "-"): v
    for k, v in os.environ.items()
    if k.startswith('HTTP_') or k in ('CONTENT_TYPE', 'CONTENT_LENGTH')
}

query_string = urllib.parse.unquote(envs['QUERY_STRING'], encoding="utf-8")
query_parameters = dict(
    pair.split('=', maxsplit=1) if '=' in pair else (pair, None)
    for pair in query_string.split('&') if pair
)

body_parameters = {}
body = sys.stdin.read()
if body:
    if headers.get('content-type') == 'application/json': body_parameters = json.loads(body)
    elif headers.get('content-type') == 'application/x-www-form-urlencoded':
        body_parameters = dict(
            pair.split('=', maxsplit=1)
            for pair in urllib.parse.unquote(body).split('&') if '=' in pair
        )
    elif headers.get('content-type', '').startswith('multipart/form-data'): body_parameters = parse_multipart_form_data(body, headers['content-type'])
    else: send_error(415, "Unsupported Media Type", "Supported types: application/json, application/x-www-form-urlencoded, multipart/form-data")

path = envs['REQUEST_URI']
if '?' in path: path = path[:path.index('?')]

response_data = {
    "status": 200,
    "method": envs['REQUEST_METHOD'],
    "query_parameters": query_parameters,
    "headers": headers,
    "body_parameters": body_parameters,
}

print("Content-Type: application/json; charset=utf-8")
print()
print(json.dumps(response_data, ensure_ascii=False, indent=2))