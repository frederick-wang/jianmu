import argparse
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path

import requests


def create(args):
    if args.project_name is None:
        print(' * The project name is required.')
        exit(0)
    project_dir: Path = args.project_name.absolute()
    project_name = project_dir.name
    if project_dir.exists():
        print(
            ' * The project directory already exists, please use a different name.'
        )
        exit(0)
    print(f' * Creating a new Jianmu project named {project_name}')
    template_url = 'https://ghproxy.com/https://github.com/frederick-wang/jianmu-template/archive/main.zip'
    print(' * Downloading the template...')
    print('(This may take a while, and the program will wait at most 30 seconds)')
    try:
        req = requests.get(template_url, timeout=30)
    except requests.exceptions.RequestException as e:
        print(e)
        print(' * Failed to download the template.')
        exit(0)
    print(' * Downloading the template completed.')
    print(' * Extracting the template...')
    with zipfile.ZipFile(BytesIO(req.content)) as template_archive:
        with tempfile.TemporaryDirectory() as tmpdir:
            template_archive.extractall(tmpdir)
            template_dir = Path(tmpdir) / 'jianmu-template-main'
            shutil.copytree(str(template_dir), str(project_dir))
            print(' * Extracting the template completed.')
    NPM_EXECUTABLE = str(shutil.which('npm'))
    if not NPM_EXECUTABLE:
        print(' * NPM is not installed.')
        exit(0)
    print(' * Installing Node.js dependencies...')
    proc = subprocess.run([
        NPM_EXECUTABLE, 'install', '--registry=https://registry.npmmirror.com'
    ],
                          cwd=str(project_dir))
    if proc.returncode:
        print(' *  Install Node.js dependencies failed.')
        exit(0)
    print('\n * Installing Node.js dependencies completed.')
    print(' * Creating the project completed. Enjoy!\n')
    print(
        'You can now start the project in development mode with following commands:\n'
    )
    print(f'cd {project_name}')
    print('jianmu dev')


def dev(args):
    CWD_PATH = Path.cwd()
    PYTHON_EXECUTABLE = sys.executable
    NPM_EXECUTABLE = str(shutil.which('npm'))
    if not NPM_EXECUTABLE:
        print(' * NPM is not installed.')
        exit(0)
    print(' * Starting the jianmu application in development mode...')
    print(f' * Current directory: {CWD_PATH}')
    JIANMU_DIR_PATH = Path(__file__).parent.resolve()
    JM_PATH = JIANMU_DIR_PATH / 'jm.py'
    env = {
        **os.environ,
        'PATH': str(CWD_PATH) + os.pathsep + os.environ['PATH'],
    }

    def clean():
        if 'flask_process' in locals():
            flask_process.terminate()
            flask_process.wait()
        if 'node_process' in locals():
            node_process.terminate()
            node_process.wait()
        sys.exit(0)

    try:
        flask_process = subprocess.Popen(args=[PYTHON_EXECUTABLE,
                                               str(JM_PATH)],
                                         cwd=str(CWD_PATH),
                                         env=env)
        node_process = subprocess.Popen(args=[NPM_EXECUTABLE, 'run', 'dev'],
                                        cwd=str(CWD_PATH),
                                        env=env)
    except Exception as e:
        print(e)
        print(' * Failed to start the jianmu application.')
        clean()

    signal.signal(signal.SIGINT, lambda signal_num, frame: clean())

    while True:
        try:
            flask_process.wait(timeout=1)
            node_process.wait(timeout=1)
            break
        except subprocess.TimeoutExpired:
            if flask_process.poll() is not None or node_process.poll(
            ) is not None:
                print(f'flask_process.poll(): {flask_process.poll()}')
                print(f'node_process.poll(): {node_process.poll()}')
                break
        except KeyboardInterrupt:
            break

    clean()


def start(args):
    print(' * The start command has not been implemented yet.')


def build(args):
    print(' * The build command has not been implemented yet.')


def default(args):
    parser.print_help()


parser = argparse.ArgumentParser(
    prog='jianmu',
    description=
    'A simple desktop app development framework combining Python, Vue.js, Element Plus and Electron.',
)
parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
parser.set_defaults(func=default)
subparsers = parser.add_subparsers()
parser_create = subparsers.add_parser('create',
                                      help='Create a new jianmu project.')
parser_create.add_argument('project_name',
                           nargs='?',
                           type=Path,
                           help='The directory name of the new project.')
parser_create.set_defaults(func=create)
parser_dev = subparsers.add_parser(
    'dev', help='Run the jianmu application in development mode.')
parser_dev.set_defaults(func=dev)
parser_start = subparsers.add_parser(
    'start', help='Run the jianmu application in production mode.')
parser_start.set_defaults(func=start)
parser_build = subparsers.add_parser('build',
                                     help='Build the jianmu application.')
parser_build.set_defaults(func=build)


def parse():
    args = parser.parse_args()
    args.func(args)
