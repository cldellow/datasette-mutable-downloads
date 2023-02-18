from setuptools import setup
import os

VERSION = "0.1.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-mutable-downloads",
    description="Enable downloading mutable databases.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Colin Dellow",
    url="https://github.com/cldellow/datasette-mutable-downloads",
    project_urls={
        "Issues": "https://github.com/cldellow/datasette-mutable-downloads/issues",
        "CI": "https://github.com/cldellow/datasette-mutable-downloads/actions",
        "Changelog": "https://github.com/cldellow/datasette-mutable-downloads/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License"
    ],
    version=VERSION,
    packages=["datasette_mutable_downloads"],
    entry_points={"datasette": ["mutable_downloads = datasette_mutable_downloads"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "pytest-watch"]},
    python_requires=">=3.7",
)
