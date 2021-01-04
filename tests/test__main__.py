"""Integration tests for YamlTable's command line interface."""


import pathlib
import pprint
from unittest.mock import call, MagicMock

import pytest
from typer import testing
import yaml

import yamltable
import yamltable.__main__ as main
from yamltable.typing import ExitCode


@pytest.mark.functional
def test_index(console: MagicMock) -> None:
    """Ensure correct stdout for index command."""

    runner = testing.CliRunner()
    result = runner.invoke(main.app, ["index", "2", "tests/data/path.yaml"])

    expected = pprint.pformat(
        {
            "name": "bash-profile",
            "dest": "$HOME/.bash_profile",
            "description": "BASH settings",
            "source": None,
            "type": "file",
        },
        indent=2,
    )

    assert result.exit_code == ExitCode.SUCCESS.value
    console.print.assert_called_once_with(expected)


@pytest.mark.functional
def test_index_error() -> None:
    """Ensure correct exit code for erroneous index command invocation."""

    runner = testing.CliRunner()
    result = runner.invoke(main.app, ["index", "20", "tests/data/path.yaml"])

    assert result.exit_code == ExitCode.ERROR.value


@pytest.mark.functional
def test_load_data_error() -> None:
    """Ensure correct exit code when loading badly formatted YAML file."""

    runner = testing.CliRunner()
    result = runner.invoke(
        main.app, ["list", "name", "tests/data/bad_format.yaml"]
    )

    assert result.exit_code == ExitCode.ERROR.value


@pytest.mark.functional
def test_list(console: MagicMock) -> None:
    """Ensure correct stdout for list command."""

    runner = testing.CliRunner()
    result = runner.invoke(main.app, ["list", "name", "tests/data/path.yaml"])

    expected = [
        call("repo"),
        call("ssh"),
        call("bash-profile"),
        call("system"),
        call("bash-key"),
        call("drive"),
        call("vscode-settings"),
        call("vscode-keybindings"),
        call("vscode-snippets"),
    ]

    assert result.exit_code == ExitCode.SUCCESS.value

    console.print.assert_has_calls(expected)


@pytest.mark.functional
def test_list_error() -> None:
    """Ensure correct exit code for erroneous list command invocation."""

    runner = testing.CliRunner()
    result = runner.invoke(
        main.app, ["list", "bad_name", "tests/data/path.yaml"]
    )

    assert result.exit_code == ExitCode.ERROR.value


@pytest.mark.functional
def test_search() -> None:
    """Ensure correct stdout for search command."""

    runner = testing.CliRunner()
    result = runner.invoke(
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
    actual = result.stdout.strip()

    assert result.exit_code == ExitCode.SUCCESS.value
    assert actual == expected


@pytest.mark.functional
def test_search_empty() -> None:
    """Ensure correct stdout for search command with no results."""

    runner = testing.CliRunner()
    result = runner.invoke(
        main.app, ["search", "name", "missing", "tests/data/path.yaml"]
    )

    expected = "No rows found with (key=name, value=missing) pair."
    actual = result.stdout.strip()

    assert result.exit_code == ExitCode.SUCCESS.value
    assert actual == expected


@pytest.mark.functional
def test_sort(tmp_path: pathlib.Path) -> None:
    """Ensure correct stdout for sort command."""

    data = [{"name": "second"}, {"name": "first"}]
    file_path = tmp_path / "path.yaml"
    with file_path.open("w") as handle:
        yaml.dump(data, handle)

    runner = testing.CliRunner()
    result = runner.invoke(main.app, ["sort", "name", str(file_path)])

    expected = [data[1], data[0]]
    with file_path.open("r") as handle:
        actual = yaml.safe_load(handle)

    assert result.exit_code == ExitCode.SUCCESS.value
    assert actual == expected


@pytest.mark.functional
def test_sort_error(tmp_yaml: pathlib.Path) -> None:
    """Ensure correct exit code for erroneous search command invocation."""

    runner = testing.CliRunner()
    result = runner.invoke(main.app, ["sort", "dest", str(tmp_yaml)])

    assert result.exit_code == ExitCode.ERROR.value


@pytest.mark.functional
def test_validate() -> None:
    """Ensure correct exit code for validate command."""

    runner = testing.CliRunner()
    result = runner.invoke(main.app, ["validate", "tests/data/path.yaml"])

    assert result.exit_code == ExitCode.SUCCESS.value


@pytest.mark.functional
def test_validate_bad_schema() -> None:
    """Ensure correct exit code for validating bad schemas."""

    runner = testing.CliRunner()
    result = runner.invoke(main.app, ["validate", "tests/data/bad_schema.yaml"])

    assert result.exit_code == ExitCode.ERROR.value


@pytest.mark.functional
def test_validate_invalid_row() -> None:
    """Ensure correct exit code for validating invalid row."""

    runner = testing.CliRunner()
    result = runner.invoke(
        main.app, ["validate", "tests/data/invalid_row.yaml"]
    )

    assert result.exit_code == ExitCode.INVALID.value


@pytest.mark.functional
def test_version() -> None:
    """Ensure display of project version."""

    runner = testing.CliRunner()
    result = runner.invoke(main.app, ["version"])

    expected = f"yamltable {yamltable.__version__}"
    actual = result.stdout.strip()

    assert result.exit_code == ExitCode.SUCCESS.value
    assert actual == expected
