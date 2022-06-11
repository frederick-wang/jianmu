from pathlib import Path
import sys

version = '0.0.8'

python_executable = sys.executable

python_executable_dir = str(Path(sys.executable).parent.resolve().absolute())

python_version = sys.version

python_version_info = sys.version_info

platform = sys.platform

cwd = str(Path.cwd().resolve().absolute())

jianmu_dir = str(Path(__file__).parent.resolve().absolute())

project_dir = cwd

jianmu_info = {
    'version': version,
    'python_executable': python_executable,
    'python_executable_dir': python_executable_dir,
    'python_version': python_version,
    'python_version_info': python_version_info,
    'platform': platform,
    'cwd': cwd,
    'jianmu_dir': jianmu_dir,
    'project_dir': project_dir,
}
