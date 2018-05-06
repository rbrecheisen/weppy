import json


class ArgParser(object):

    def __init__(self):
        self.args = {}
        self.args_mandatory = []

    def add_arg(self, name, optional=False):
        if name.startswith('--'):
            name = name[2:]
        self.args[name] = None
        if not optional:
            self.args_mandatory.append(name)

    def parse_args(self, args):
        if len(args) != len(self.args_mandatory):
            raise RuntimeError('Number of mandatory arguments does not match')
        for arg in args:
            print(arg)
            name, value = arg.split('=')[0], arg.split('=')[1]
            if name.startswith('--'):
                name = name[2:]
            if name.startswith('-'):
                name = name[1:]
            if name not in self.args.keys():
                raise RuntimeError('Argument {} not in {}'.format(name, self.args.keys()))
            if value.startswith('{') and value.endswith('}'):
                value = json.loads(value)
            self.args[name] = value
        return self.args

    def print(self, indent=4):
        print('Arguments:')
        print(json.dumps(self.args, indent=indent))
