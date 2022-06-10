from argparse import ArgumentParser
from pathlib import Path
from shutil import rmtree


def init_parser(subparsers):
    parser: ArgumentParser = subparsers.add_parser(
        'clean', help='Clean runtime temporary files in project directory.')
    parser.set_defaults(func=__func)


def __func(args):
    CWD_PATH = Path.cwd()
    TMP_DIR_PATH = CWD_PATH / '.jianmu'
    print(' * Cleaning runtime temporary files...')
    rmtree(str(TMP_DIR_PATH), ignore_errors=True)
    print(' * Runtime temporary files have been cleaned.')
