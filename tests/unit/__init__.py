"""Unit test functions from the yamltable module."""


from typing import List

import pytest

import yamltable
from yamltable.typing import Row, Schema


@pytest.mark.parametrize(
    "file_data",
    ["false", "mock_key_1: 1\nmock_key_2: 5", "mock_key_1: 1\n- mock_key_2: 5"],
)
def test_read_bad_data(file_data: str) -> None:
    """Check that reader throws an exception when reading invalid YAML file."""
    with pytest.raises(TypeError):
        yamltable.read(file_data)


@pytest.mark.parametrize(
    "file_data,expected",
    [
        ("- mock_key: 1\n- mock_key: 5", [{"mock_key": 1}, {"mock_key": 5}]),
        ("schema:\n  type: object\nrows:\n- mock_key: 1", [{"mock_key": 1}]),
    ],
)
def test_read_good_data(file_data: str, expected: List[Row]) -> None:
    """Check that reader correctly reads data that is a list."""
    actual, _ = yamltable.read(file_data)

    assert actual == expected


def test_search() -> None:
    """Check that searching works for unnested list of dictionaries."""
    dicts = [
        {"mock_key_1": 1, "mock_key_2": 5},
        {"mock_key_1": 2, "mock_key_2": 3},
    ]

    expected = [{"mock_key_1": 2, "mock_key_2": 3}]
    actual = yamltable.search("mock_key_2", 3, dicts)
    assert actual == expected


def test_sort() -> None:
    """Check that sorting works for unnested list of dictionaries."""
    dicts = [
        {"mock_key_1": 1, "mock_key_2": 5},
        {"mock_key_1": 2, "mock_key_2": 3},
    ]

    expected = [
        {"mock_key_1": 2, "mock_key_2": 3},
        {"mock_key_1": 1, "mock_key_2": 5},
    ]
    actual = yamltable.sort("mock_key_2", dicts)
    assert actual == expected


def test_dependencies() -> None:
    """Check that dependencies are resolved."""
    dicts = [
        {"name": 1, "depends": [2]},
        {"name": 2, "depends": []},
    ]

    expected = [
        {"name": 2, "depends": []},
        {"name": 1, "depends": [2]},
    ]

    actual = yamltable.dependencies(dicts, "depends", "name")
    assert actual == expected


def test_dependencies_circular_error() -> None:
    """Check that error is raised when a circular dependency is encountered."""
    dicts = [
        {"name": 1, "depends": [2]},
        {"name": 2, "depends": [1]},
    ]

    with pytest.raises(ValueError):
        yamltable.dependencies(dicts, "depends", "name")


def test_validate_bad_schema() -> None:
    """Check that validation works for unnested list of dictionaries."""
    schema_ = {"type": "data"}
    dicts = [
        {"mock_key_1": 1, "mock_key_2": 5},
        {"mock_key_1": 2, "mock_key_2": 3},
    ]

    expected = (False, -1, "'data' is not valid under any of the given schemas")
    result = yamltable.validate(dicts, schema_)
    actual = (result[0], result[1], result[2].split("\n")[0])
    assert actual == expected


def test_validate_bad_data(schema: Schema) -> None:
    """Check that validation works for unnested list of dictionaries."""
    dicts = [
        {"mock_key_1": 1, "mock_key_2": 5},
        {"mock_key_1": 2, "mock_key_2": False},
    ]

    expected = (False, 1, "False is not of type 'number'")
    result = yamltable.validate(dicts, schema)
    actual = (result[0], result[1], result[2].split("\n")[0])
    assert actual == expected


def test_validate_good_data(schema: Schema) -> None:
    """Check that validation works for unnested list of dictionaries."""
    dicts = [
        {"mock_key_1": 1, "mock_key_2": 5},
        {"mock_key_1": 2, "mock_key_2": 3},
    ]

    expected = (True, -1, "")
    actual = yamltable.validate(dicts, schema)
    assert actual == expected
