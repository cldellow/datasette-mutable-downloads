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

You can now download a mutable database on its database page, just as you
can for immutable databases.

Example: https://dux.fly.dev/cooking

## Notes

This is achieved by a somewhat gross monkeypatch of the `DatabaseDownload`
view.

We detect if the database is mutable. If it is, we first create a copy via
[`VACUUM INTO`](https://www.sqlite.org/lang_vacuum.html#vacuum_with_an_into_clause).

We then stream that file to the user, and delete it.

This requires SQLite 3.27.0 or newer (Feb 2019).

> **NOTE**
>
> The act of `VACUUM INTO` could be resource intensive if your
> database is large. If you expose your Datasette to the Internet,
> you may wish to restrict this to only authenticated users.
>
> To do that, add a permissions block in your metadata.json:
> 
> permissions: { "view-database-download": { "gh_id": "*" } }

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-mutable-downloads
    python3 -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
