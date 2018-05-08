from weppy.utils import ArgParser


arg_parser = ArgParser()
arg_parser.add_arg('in_file', arg_type='file')
arg_parser.add_arg('in_dir', arg_type='dir')


def run(args):
    args = arg_parser.parse_args(args)
    print('hello_world.py: {}'.format(args))
