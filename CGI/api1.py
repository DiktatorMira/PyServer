import codecs
import json
import os
import sys
import urllib.parse

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdin  = codecs.getreader("utf-8")(sys.stdin.detach())

def send_error(code:int=400, phrase:str="Bad Request", explain:str=None) :
    print("Status: %d %s" % (code, phrase))
    print("Content-Type: text/plain; charset=utf-8")
    print()
    print(explain if explain != None else phrase, end='')
    exit()

envsUl = "<ul>" + ''.join( "<li>%s = %s</li>" % (k,v) 
    for k,v in os.environ.items() ) + "</ul>"
envs = { k: v for k,v in os.environ.items() if k in ('REQUEST_METHOD','QUERY_STRING','REQUEST_URI') }

headers = { (k[5:] if k.startswith('HTTP_') else k).lower().replace("_","-"): v 
    for k,v in os.environ.items() 
    if k.startswith('HTTP_') or k in ('CONTENT_TYPE', 'CONTENT_LENGTH') }

query_string = urllib.parse.unquote( envs['QUERY_STRING'], encoding="utf-8" )
query_parameters = dict( pair.split('=', maxsplit = 1) if '=' in pair else (pair, None)
                    for pair in query_string.split('&') if pair != "" )

body_parameters = {}
body = sys.stdin.read()

if body != '' :
    if headers['content-type'] == 'application/json' : body_parameters = json.loads( body )
    elif headers['content-type'] == 'application/x-www-form-urlencoded' :
        body_parameters = dict( pair.split('=', maxsplit = 1) 
        for pair in urllib.parse.unquote(body).split('&') if '=' in pair  )
    else : send_error( 415, "Unsupported Media Type", "Supported MIME: 'application/json' , 'application/x-www-form-urlencoded'" )        

path = envs['REQUEST_URI']
if '?' in path : path = path[:(path.index('?'))]

print( "Content-Type: application/json; charset=utf-8" )
print()
print( json.dumps(body_parameters, ensure_ascii=False), end="" )