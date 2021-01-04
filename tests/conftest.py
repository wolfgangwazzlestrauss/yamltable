"""Reusable testing fixtures for YamlTable."""


import pathlib
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture

import yamltable.__main__ as main
from yamltable.typing import Schema


@pytest.fixture
def console(mocker: MockFixture) -> MagicMock:
    """Replaces Rich console in CLI with a magic mock.

    Return:
        Magic mock instance.
    """

    main.console = MagicMock()
    return main.console


@pytest.fixture(scope="module")
def schema() -> Schema:
    """Create reusable JSON schema object.

    Return:
        JSON schema dictionary
    """

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "mock_key_1": {"type": "number"},
            "mock_key_2": {"type": "number"},
        },
        "required": ["mock_key_1", "mock_key_2"],
        "additionalProperties": False,
    }


@pytest.fixture
def tmp_yaml(tmp_path: pathlib.Path) -> pathlib.Path:
    """Temporary copy of path.yaml."""

    dest_path = tmp_path / "path.yaml"
    src_path = pathlib.Path("tests/data/path.yaml")

    text = src_path.read_text()
    dest_path.write_text(text)

    return dest_path
