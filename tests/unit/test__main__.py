"""Integration tests for YamlTable's command line interface."""


import pprint

from typer import testing

import yamltable.__main__ as main


def test_search() -> None:
    """Command line test for search option."""

    runner = testing.CliRunner()
    resp = runner.invoke(
        main.app, ["search", "name", "repo", "tests/data/path.yaml"]
    )

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
