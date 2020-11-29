# BackupExtractor
A simple iDevice backup extracting tool using ```Manifest.db```

## Introduction

It supports the latest version of iOS(iPhone, iPad) backup.

## Getting Started
### Prerequisites

Make sure that you have installed [Python](https://python.org/) >=3.7 and [pip](https://pip.pypa.io/en/stable/installing/) before installation.

-   If you are using [pyenv](https://github.com/pyenv/pyenv) virtualenv, run a commands below to make separated python environment.
``` bash
$ cd backupextractor
$ pyenv install 3.7
$ pyenv virtualenv 3.7 <env_name>
$ pyenv local <env_name>
```

### Installing

``` bash
$ pip install -r requirement.txt
```

## Usage

Enter ```python backupextractor.py --help``` to get usage.
