"""Reusable testing fixtures for YamlTable."""


import pathlib

import pytest

from yamltable.typing import Schema


@pytest.fixture
def schema(scope: str = "module") -> Schema:
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
