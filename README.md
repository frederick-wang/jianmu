<div align="center">
<br>
<img width="640" src="https://raw.githubusercontent.com/frederick-wang/jianmu/main/docs/images/jianmu-preview-without-border.png" alt="Jianmu Framework">
<br>
<br>
</div>

<p align="center" color="#262626">
A simple desktop app development framework combining Python, Vue.js, Element Plus and Electron.
</p>


<p align="center">
<img src="https://img.shields.io/pypi/pyversions/Jianmu" alt="pyversions"> <img src="https://img.shields.io/pypi/v/Jianmu" alt="version"> <img src="https://img.shields.io/pypi/l/Jianmu" alt="license"> <img src="https://img.shields.io/github/last-commit/frederick-wang/jianmu" alt="last-commit"> <img src="https://img.shields.io/github/commit-activity/m/frederick-wang/jianmu" alt="commit-activity"></img>
</p>

## Installation

### Python Version

We recommend using the latest version of Python. Jianmu supports Python 3.6 and newer.

### Install Jianmu

To install the jianmu package, use the following command:

```sh
python -m pip install jianmu -U
```

Jianmu is now installed. After installation, you will have access to the `jianmu` binary in your command line. You can verify that it is properly installed by simply running `jianmu` command or `python -m jianmu`, which should present you with a help message listing all available commands.

You can check you have the right version with this command:

```sh
jianmu --version
```

## Usage

To create a new project, run:

```sh
jianmu create <project-name>
```

To upgrade the template of your project, navigate to the project directory and run:

```sh
jianmu upgrade
```

To run your application in development mode, navigate to your project directory and run:

```sh
jianmu dev
```

To run your application in production mode, navigate to your project directory and run:

```sh
jianmu start
```

To build your application for a software release, navigate to your project directory and run:

```sh
jianmu build
```

To clean runtime temporary files in project directory, navigate to your project directory and run:

```sh
jianmu clean
```
