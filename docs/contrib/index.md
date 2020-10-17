# Developer Guide

Thank you for taking the time to contribute to the YamlTable project. This guide
will assist you in setting up a development environment, understanding the
project tooling, and learning the coding guidelines.

## Environment

### Local

## Coding Guidelines

When contributing to YamlTable, please follow the
[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
An example, of the Python Google docstring style, can be found at
https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html.

Type hints are heavily enforced in this repository. The CI pipeline will reject
any pull request that does not provide type hints for every function and method.
Mypy's [cheat sheet](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html)
is an excellent reference for quick type hinting help.

Similarilt, 100% test coverage is enforced by the CI pipeline.

## Documentation

YamlTable documentation exists in the repository's `docs` folder
