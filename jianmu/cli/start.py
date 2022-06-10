from argparse import ArgumentParser


def init_parser(subparsers):
    parser: ArgumentParser = subparsers.add_parser(
        'start', help='Run the jianmu application in production mode.')
    parser.set_defaults(func=__func)


def __func(args):
    print(' * The start command has not been implemented yet.')
