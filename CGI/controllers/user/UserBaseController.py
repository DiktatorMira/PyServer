import json
import sys
from data.user_dao import User
from controllers.ApiController import ApiController

class UserBaseController(ApiController):
    def __init__(self):
        super().__init__()
        self.response.meta.add('ctr', 'UserBaseController')

    def do_get(self):
        users = UserDao().get_all_users()
        response_data = [user.to_dict() for user in users]
        self.send_json(RestModel(RestStatus.SUCCESS, RestMeta(), response_data))

    def do_post(self):
        db_context = self.am_data.db_context
        user_dao = db_context.user_dao
        body = sys.stdin.read()
        if len(body) < 3: self.end_with(400, "Body must not be empty")

        try: j = json.loads(body)
        except ValueError: self.end_with(400, "Invalid JSON")
        try:
            user = User(
                name=j['user-name'],
                email=j['user-email'],
                password=j['user-password']
            )
        except ValueError: self.end_with(422, "Body must have props: 'user-name', 'user-email', 'user-password'" )

        if not user_dao.is_login_free(user.email): self.end_with(422, " 'user-email' in use")

        user_dao.add_user(user)
        return "User Created"