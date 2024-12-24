import codecs
import sys
from am_data import AmData

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

def send_error(code=400, phrase="Bad Request", explain=None):
    print(f"Status: {code} {phrase}")
    print("Access-Control-Allow-Origin: *")
    print("Content-Type: text/plain; charset=utf-8")
    print()
    print(explain if explain else phrase)
    exit()

def send_file( filename:str ) :
    print( "Content-Type: text/html; charset=utf-8" )
    print()
    with open( filename, encoding="utf-8" ) as file : print( file.read() )
    exit()

def ucfirst( input:str ) :
    if len( input ) == 0 : return input
    if len( input ) == 1 : return input[0].upper()
    return input[0].upper() + input[1:].lower()

import os
envs = {
    k: v for k, v in os.environ.items()
    if k in ('REQUEST_METHOD', 'QUERY_STRING', 'REQUEST_URI')
}
routes = { '/api/users': UserBaseController, }
path = envs['REQUEST_URI']
if '?' in path: path = path[:path.index('?')]
if path.startswith( '/' ): path = path[1:]
if path == '': send_file("homepage.html")

parts = path.split('/', maxsplit=2)
controller = parts[0]
category = parts[1] if len(parts) > 1 and len(parts[1]) > 0 else 'base'
slug = parts[2] if len(parts) > 2 else None

controller_name = ucfirst(controller) + ucfirst(category) + "Controller"
sys.path.append('./')
import importlib

try :
    controller_module = importlib. import_module( f'controllers.{controller}.{controller_name}')
    controller_class = getattr( controller_module, controller_name )
    controller_object = controller_class()
    controller_action = getattr( controller_object, "serve" )
    controller_action(AmData(envs, path, controller,category, slug) )
except Exception as err : send_error( explain=err )