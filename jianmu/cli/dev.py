import os
import shutil
import signal
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path


def init_parser(subparsers):
    parser: ArgumentParser = subparsers.add_parser(
        'dev', help='Run the jianmu application in development mode.')
    parser.set_defaults(func=__func)


def __func(args):
    CWD_PATH = Path.cwd()
    PYTHON_EXECUTABLE = sys.executable
    NPM_EXECUTABLE = str(shutil.which('npm'))
    PROJECT_LOG_DIR_PATH = CWD_PATH / '.jianmu' / 'logs'
    PROJECT_LOG_DIR_PATH.mkdir(parents=True, exist_ok=True)
    JM_LOG_PATH = PROJECT_LOG_DIR_PATH / 'jm.log'
    f_jm_log = open(JM_LOG_PATH, 'w', encoding='utf-8')
    if not NPM_EXECUTABLE:
        print(' * NPM is not installed.')
        exit(0)
    print(' * Starting the jianmu application in development mode...')
    print(f' * Current directory: {CWD_PATH}')
    JIANMU_DIR_PATH = Path(__file__).parent.parent.resolve()
    JM_PATH = JIANMU_DIR_PATH / 'jm.py'
    env = {
        **os.environ,
        'PATH': str(CWD_PATH) + os.pathsep + os.environ['PATH'],
        'DEBUGGING': 'true',
    }
    flask_process: subprocess.Popen[bytes]

    def clean():
        if 'flask_process' in locals() and flask_process.poll() is None:
            flask_process.terminate()
            flask_process.wait()
        if 'node_process' in locals() and node_process.poll() is None:
            node_process.terminate()
            node_process.wait()
        print(' * The jianmu application has been stopped.')
        exit(0)

    try:
        flask_process = subprocess.Popen(args=[PYTHON_EXECUTABLE,
                                               str(JM_PATH)],
                                         cwd=str(CWD_PATH),
                                         env=env,
                                         stdout=f_jm_log,
                                         stderr=f_jm_log)
    except Exception as e:
        print(e)
        print(' * Failed to start the jianmu application.')
        exit(0)

    try:
        node_process = subprocess.Popen(args=['node', 'scripts/dev-server.js'],
                                        cwd=str(CWD_PATH),
                                        env=env)
    except Exception as e:
        print(e)
        print(' * Failed to start the jianmu application.')
        flask_process.terminate()
        flask_process.wait()
        exit(0)

    def on_sigint(signum, frame):
        clean()

    signal.signal(signal.SIGINT, on_sigint)

    while True:
        try:
            flask_process.wait(timeout=1)
            node_process.wait(timeout=1)
            break
        except subprocess.TimeoutExpired:
            if flask_process.poll() is not None or node_process.poll(
            ) is not None:
                break
        except KeyboardInterrupt:
            break

    clean()
