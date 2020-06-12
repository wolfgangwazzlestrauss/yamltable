"""Reusable testing fixtures for YamlTable unit tests."""


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