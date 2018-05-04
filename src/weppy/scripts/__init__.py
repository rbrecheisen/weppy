class Script(object):

    def __init__(self):
        self.name = ''
        self.display_name = ''
        self.args = None

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_display_name(self, display_name):
        self.display_name = display_name

    def get_display_name(self):
        return self.display_name

    def set_args(self, args):
        self.args = args

    def get_args(self):
        return self.args

    def run(self):
        raise NotImplemented()
