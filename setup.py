from setuptools import setup
import setuptools

from jianmu.info import version

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='Jianmu',
    version=version,
    description=
    'A simple desktop app development framework combining Python, Vue.js, Element Plus and Electron.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Zhaoji Wang',
    author_email='hwoam@outlook.com',
    url='https://github.com/frederick-wang/jianmu',
    project_urls={
        "Bug Tracker": "https://github.com/frederick-wang/jianmu/issues",
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'Flask',
        'requests',
    ],
    packages=setuptools.find_packages(include=['jianmu', 'jianmu.*']),
    entry_points={
        'console_scripts': ['jianmu=jianmu.cli:parse'],
    },
    python_requires=">=3.6, <=3.10",
)
