from argparse import ArgumentParser


def init_parser(subparsers):
    parser: ArgumentParser = subparsers.add_parser(
        'build', help='Build the jianmu application.')
    parser.set_defaults(func=__func)


def __func(args):
    print(' * The build command has not been implemented yet.')
