from controllers.ApiController import ApiController

class UserAuthController( ApiController ) :

    def do_get(self) : return { 'user-auth': 'works' }