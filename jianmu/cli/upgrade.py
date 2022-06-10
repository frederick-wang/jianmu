from argparse import ArgumentParser


def init_parser(subparsers):
    parser: ArgumentParser = subparsers.add_parser(
        'upgrade', help='Upgrade the template of Jianmu Application.')
    parser.set_defaults(func=__func)


def __func(args):
    print(' * The upgrade command has not been implemented yet.')
