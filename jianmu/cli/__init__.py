import argparse

from ..info import version
from . import build
from . import create
from . import dev
from . import start

parser = argparse.ArgumentParser(
    prog='jianmu',
    description=
    'A simple desktop app development framework combining Python, Vue.js, Element Plus and Electron.',
)


def parse():
    init_parser()
    args = parser.parse_args()
    args.func(args)


def init_parser():
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version=f'%(prog)s {version}')
    parser.set_defaults(func=__func)

    subparsers = parser.add_subparsers()
    create.init_parser(subparsers)
    dev.init_parser(subparsers)
    start.init_parser(subparsers)
    build.init_parser(subparsers)


def __func(args):
    parser.print_help()


__all__ = ['parse']
