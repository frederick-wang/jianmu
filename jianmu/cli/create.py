import os
import shutil
import subprocess
import tempfile
import zipfile
from argparse import ArgumentParser
from io import BytesIO
from pathlib import Path

import requests


def init_parser(subparsers):
    parser: ArgumentParser = subparsers.add_parser(
        'create', help='Create a new jianmu project.')
    parser.add_argument('project_name',
                        nargs='?',
                        type=Path,
                        help='The directory name of the new project.')
    parser.set_defaults(func=__func)


def __func(args):
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
    print(
        ' * (This may take a while, and the program will wait at most 30 seconds)'
    )
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
    env = {
        **os.environ,
        'ELECTRON_MIRROR':
            'https://npmmirror.com/mirrors/electron/',
    }
    proc = subprocess.run(
        [
            NPM_EXECUTABLE, 'install',
            '--registry=https://registry.npmmirror.com'
        ],
        cwd=str(project_dir),
        env=env,
    )
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
