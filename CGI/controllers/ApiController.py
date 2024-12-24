import json
from models.RestModel import *
from am_data import AmData

class ApiController:
    def __init__(self):
        self.response = RestModel()
        self.response.meta = RestMeta({
            'service': 'Server Application',
            'group': 'KN-P-213',
        })

    def end_with(self, status_code: int = 200, data: any = None):
        if status_code != 200: self.response.status = RestStatus(status_code)
        print("Status: %d %s" % (status_code, self.response.status.reasonPhrase))
        self.response.data = data
        print("Access-Control-Allow-Origin: *")
        print("Access-Control-Allow-Headers: content-type")
        print("Content-Type: text/plain; charset=utf-8")
        print()
        print(json.dumps(self.response, default=vars))
        exit()

    def serve(self, am_data: AmData):
        self.am_data = am_data
        method = am_data.envs["REQUEST_METHOD"]
        self.response.meta.add('method', method)
        action_name = f"do_{method.lower()}"
        controller_action = getattr(self, action_name, None)
        if controller_action == None: self.end_with(405, f"Method '{am_data.envs["REQUEST_METHOD"]}' not supported")
        else: self.end_with(data=controller_action())

    def do_options(self):
        '''CORS/CORP - info about supported items'''
        print("Access-Control-Allow-Origin: *")
        print("Access-Control-Allow-Methods: GET, POST, PUT, DELETE")
        print("Access-Control-Allow-Headers: content-type")
        print()
        exit()