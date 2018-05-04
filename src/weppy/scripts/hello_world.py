import sys
from weppy.utils import ArgParser
from weppy.scripts import Script


class HelloWorld(Script):

    def run(self):

        arg_parser = ArgParser()
        arg_parser.add_arg('in_file')
        args = arg_parser.parse_args(self.get_args())
        arg_parser.print()


if __name__ == '__main__':

    script = HelloWorld()
    script.set_args(sys.argv)
    script.run()
