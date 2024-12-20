import json
from models.RestModel import *

class ApiController :
    def __init__(self):
        self.response = RestModel()        
        self.response.meta = RestMeta({
            'service': 'Server Application',
            'group': 'KN-P-213'
        })

    def end_with( self, status_code:int=200, data:any=None ) :
        if status_code != 200 :
            self.response.status = RestStatus(status_code)
            print( "Status: %d %s" % (status_code, self.response.status.reasonPhrase ) )
        self.response.data = data
        print( "Content-Type: application/json; charset=utf-8" )
        print()
        print( json.dumps( self.response, default=vars ) )
        exit()


    def serve( self, am_data ) :
        self.am_data = am_data
        method = am_data["envs"]["REQUEST_METHOD"]
        self.response.meta.add( 'method', method )
        action_name = f"do_{method.lower()}"
        controller_action = getattr( self, action_name, None )
        if controller_action == None : self.end_with( 405, f"Method '{method}' not supported in requested endpoint" )
        else :self.end_with( data=controller_action() )

'''
Д.З. Додати до meta-інформації контролерів усі Query-параметри, що
надходять разом із запитом
{
  "status": {
    "statusCode": 200,
    "reasonPhrase": "OK",
    "isSuccess": true
  },
  "meta": {
    "service": "Server Application",
    "group": "KN-P-213",
    "ctr": "UserBaseController",
    "method": "GET",
    ************************************************
    "params": {"x": 10, "y": 20, "json": null}
    *************************************************
  },
  "data": {
    "user": "works"
  }
}
'''