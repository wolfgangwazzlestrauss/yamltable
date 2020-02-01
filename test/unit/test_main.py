"""Integration tests for YamlTable's command line interface."""


import pathlib
import pprint

import toml
from typer import testing

import yamltable
from yamltable import main


def test_yamltable_version() -> None:
    """Check that all the version tags are in sync."""

    pyproject_path = pathlib.Path(yamltable.__file__).parents[2] / "pyproject.toml"
    expected = toml.load(pyproject_path)["tool"]["poetry"]["version"]

    actual = yamltable.__version__
    assert actual == expected


def test_search() -> None:
    """Command line test for search option."""

    runner = testing.CliRunner()
    resp = runner.invoke(main.app, ["search", "name", "repo", "test/data/path.yaml"])

    expected = pprint.pformat(
        {
            "name": "repo",
            "dest": "$HOME/repo",
            "description": "GitHub repository directory",
            "type": "directory",
            "source": None,
        },
        indent=2,
    )
    actual = resp.stdout.strip()

    assert resp.exit_code == 0
    assert actual == expected
