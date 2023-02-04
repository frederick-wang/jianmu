import shutil
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import List


def init_parser(subparsers):
    parser: ArgumentParser = subparsers.add_parser(
        'start', help='Run the jianmu application in production mode.')
    parser.set_defaults(func=__func)


def __func(args):
    NPX_PATH = shutil.which('npx')
    if not NPX_PATH:
        print(' * Node.js or NPM is not installed.')
        exit(0)
    PYTHON_PATH = sys.executable
    JIANMU_PATH = Path(__file__).parent.parent.resolve()
    PROJECT_PATH = Path.cwd()
    run_jianmu_js_args: List[str] = [
        NPX_PATH,
        'jianmu-js',
        'start',
        '--python-path',
        PYTHON_PATH,
        '--jianmu-path',
        str(JIANMU_PATH),
        '--project-path',
        str(PROJECT_PATH),
    ]
    try:
        subprocess.run(run_jianmu_js_args, cwd=PROJECT_PATH)
    except KeyboardInterrupt as e:
        print(
            ' * Getted KeyboardInterrupt, Jianmu Development Server has been stopped.'
        )
    except Exception as e:
        print(
            ' * Something went wrong, Jianmu Development Server has been stopped.'
        )
        print(e)
