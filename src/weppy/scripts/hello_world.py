from weppy.utils import ArgParser


arg_parser = ArgParser()
arg_parser.add_arg('in_file')


def get_args():
    return arg_parser.get_args()


def run(args):
    args = arg_parser.parse_args(args)
    print('hello_world.py: {}'.format(args))
