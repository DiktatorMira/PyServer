from data.db_context import DbContext

class AmData :
    def __init__(self, envs, path, controller, category, slug) :
        self.db_context = DbContext()
        self.envs = envs
        self.path = path
        self.controller = controller
        self.category = category
        self.slug = slug