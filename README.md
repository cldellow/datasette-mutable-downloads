# datasette-mutable-downloads

[![PyPI](https://img.shields.io/pypi/v/datasette-mutable-downloads.svg)](https://pypi.org/project/datasette-mutable-downloads/)
[![Changelog](https://img.shields.io/github/v/release/cldellow/datasette-mutable-downloads?include_prereleases&label=changelog)](https://github.com/cldellow/datasette-mutable-downloads/releases)
[![Tests](https://github.com/cldellow/datasette-mutable-downloads/workflows/Test/badge.svg)](https://github.com/cldellow/datasette-mutable-downloads/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/cldellow/datasette-mutable-downloads/blob/main/LICENSE)

Enable downloading mutable databases.

## Installation

Install this plugin in the same environment as Datasette.

    datasette install datasette-mutable-downloads

## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-mutable-downloads
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest