"""Unit test functions from the yamltable module."""


import pathlib
from typing import List

import pytest
import pytest_mock
import yamltable
from yamltable.typing import Row, Schema


@pytest.mark.parametrize(
    "file_data", ["false", "mock_key_1: 1\nmock_key_2: 5", "mock_key_1: 1\n- mock_key_2: 5"]
)
def test_read_bad_data(file_data: str, mocker: pytest_mock.MockFixture) -> None:
    """Check that reader throws an exception when reading invalid YAML file."""

    mocker.patch("builtins.open", mocker.mock_open(read_data=file_data))
    with pytest.raises(TypeError):
        yamltable.read(pathlib.Path("mock_file_path.yaml"))


@pytest.mark.parametrize(
    "file_data,expected",
    [
        ("- mock_key: 1\n- mock_key: 5", [{"mock_key": 1}, {"mock_key": 5}]),
        ("schema:\n  type: object\nrows:\n- mock_key: 1", [{"mock_key": 1}]),
    ],
)
def test_read_good_data(
    file_data: str, expected: List[Row], mocker: pytest_mock.MockFixture
) -> None:
    """Check that reader correctly reads data that is a list."""

    mocker.patch("builtins.open", mocker.mock_open(read_data=file_data))
    actual, _ = yamltable.read(pathlib.Path("mock_file_path.yaml"))

    assert actual == expected


def test_search() -> None:
    """Check that searching works for unnested list of dictionaries."""

    dicts = [{"mock_key_1": 1, "mock_key_2": 5}, {"mock_key_1": 2, "mock_key_2": 3}]

    expected = [{"mock_key_1": 2, "mock_key_2": 3}]
    actual = yamltable.search("mock_key_2", 3, dicts)
    assert actual == expected


def test_sort() -> None:
    """Check that sorting works for unnested list of dictionaries."""

    dicts = [{"mock_key_1": 1, "mock_key_2": 5}, {"mock_key_1": 2, "mock_key_2": 3}]

    expected = [{"mock_key_1": 2, "mock_key_2": 3}, {"mock_key_1": 1, "mock_key_2": 5}]
    actual = yamltable.sort("mock_key_2", dicts)
    assert actual == expected


def test_validate_bad_schema() -> None:
    """Check that validation works for unnested list of dictionaries."""

    schema = {"type": "data"}
    dicts = [{"mock_key_1": 1, "mock_key_2": 5}, {"mock_key_1": 2, "mock_key_2": 3}]

    expected = (False, -1, "invalid schema: Unknown type: 'data'")
    actual = yamltable.validate(dicts, schema)
    assert actual == expected


@pytest.fixture
def schema(scope: str = "module") -> Schema:
    """Create reusable JSON schema object.

    Return:
        JSON schema dictionary
    """

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"mock_key_1": {"type": "number"}, "mock_key_2": {"type": "number"}},
        "required": ["mock_key_1", "mock_key_2"],
        "additionalProperties": "false",
    }


def test_validate_bad_data(schema: Schema) -> None:
    """Check that validation works for unnested list of dictionaries."""

    dicts = [{"mock_key_1": 1, "mock_key_2": 5}, {"mock_key_1": 2, "mock_key_2": False}]

    expected = (False, 1, "data.mock_key_2 must be number")
    actual = yamltable.validate(dicts, schema)
    assert actual == expected


def test_validate_good_data(schema: Schema) -> None:
    """Check that validation works for unnested list of dictionaries."""

    dicts = [{"mock_key_1": 1, "mock_key_2": 5}, {"mock_key_1": 2, "mock_key_2": 3}]

    expected = (True, -1, "")
    actual = yamltable.validate(dicts, schema)
    assert actual == expected


if __name__ == "__main__":
    pytest.main()
