from controllers.ApiController import ApiController

class UserBaseController(ApiController):

    def __init__(self):
        super().__init__()
        self.response.meta.add('ctr', 'UserBaseController')

    def do_get(self):
        query_params = self.am_data.get("envs", {}).get("QUERY_STRING", "")
        parsed_params = dict(
            pair.split('=', maxsplit=1) if '=' in pair else (pair, None)
            for pair in query_params.split('&') if pair
        )
        self.response.meta.add('params', parsed_params)
        return {'user': 'works'}
