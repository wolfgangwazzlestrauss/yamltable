"""Testing package for yamltable."""


import pathlib
from typing import List

import pytest
import pytest_benchmark.fixture as bm
import toml

import yamltable
from yamltable.typing import Row, Schema


@pytest.mark.unit
def test_dependencies(benchmark: bm.BenchmarkFixture) -> None:
    """Check that dependencies are resolved."""

    dicts = [
        {"name": 1, "depends": [2]},
        {"name": 2, "depends": []},
    ]

    expected = [
        {"name": 2, "depends": []},
        {"name": 1, "depends": [2]},
    ]

    actual = benchmark(yamltable.dependencies, dicts, "depends", "name")
    assert actual == expected


@pytest.mark.unit
def test_dependencies_circular_error() -> None:
    """Check that error is raised when a circular dependency is encountered."""

    dicts = [
        {"name": 1, "depends": [2]},
        {"name": 2, "depends": [1]},
    ]

    with pytest.raises(ValueError):
        yamltable.dependencies(dicts, "depends", "name")


@pytest.mark.unit
@pytest.mark.parametrize(
    "file_data",
    ["false", "mock_key_1: 1\nmock_key_2: 5", "mock_key_1: 1\n- mock_key_2: 5"],
)
def test_read_bad_data(file_data: str) -> None:
    """Check that reader throws an exception when reading invalid YAML file."""

    with pytest.raises(TypeError):
        yamltable.read(file_data)


@pytest.mark.unit
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


@pytest.mark.unit
def test_search(benchmark: bm.BenchmarkFixture) -> None:
    """Check that searching works for unnested list of dictionaries."""

    dicts = [
        {"mock_key_1": 1, "mock_key_2": 5},
        {"mock_key_1": 2, "mock_key_2": 3},
    ]

    expected = [{"mock_key_1": 2, "mock_key_2": 3}]
    actual = benchmark(yamltable.search, "mock_key_2", 3, dicts)
    assert actual == expected


@pytest.mark.unit
def test_sort(benchmark: bm.BenchmarkFixture) -> None:
    """Check that sorting works for unnested list of dictionaries."""

    dicts = [
        {"mock_key_1": 1, "mock_key_2": 5},
        {"mock_key_1": 2, "mock_key_2": 3},
    ]

    expected = [
        {"mock_key_1": 2, "mock_key_2": 3},
        {"mock_key_1": 1, "mock_key_2": 5},
    ]
    actual = benchmark(yamltable.sort, "mock_key_2", dicts)
    assert actual == expected


@pytest.mark.integration
def test_sort_dict(tmp_path: pathlib.Path) -> None:
    """Test sorting and overwriting file."""

    yaml_file = tmp_path / "file.yaml"
    yaml_file.write_text(
        "schema:\n  type: object\n"
        "rows:\n- foo: 1\n  bar: 4\n- foo: 3\n  bar: 2\n"
    )

    dicts, schema = yamltable.read(yaml_file)
    sorted_dicts = yamltable.sort("bar", dicts)
    yamltable.write(yaml_file, sorted_dicts, schema)

    expected = (
        "schema:\n  type: object\n"
        "rows:\n- foo: 3\n  bar: 2\n- foo: 1\n  bar: 4\n"
    )
    actual = yaml_file.read_text()
    assert actual == expected


@pytest.mark.integration
def test_sort_list(tmp_path: pathlib.Path) -> None:
    """Test sorting and overwriting file."""

    yaml_file = tmp_path / "file.yaml"
    yaml_file.write_text("- foo: 1\n  bar: 4\n- foo: 3\n  bar: 2\n")

    dicts, _ = yamltable.read(yaml_file)
    sorted_dicts = yamltable.sort("bar", dicts)
    yamltable.write(yaml_file, sorted_dicts)

    expected = "- foo: 3\n  bar: 2\n- foo: 1\n  bar: 4\n"
    actual = yaml_file.read_text()
    assert actual == expected


@pytest.mark.unit
def test_validate_bad_schema(benchmark: bm.BenchmarkFixture) -> None:
    """Check that validation works for unnested list of dictionaries."""

    schema_ = {"type": "data"}
    dicts = [
        {"mock_key_1": 1, "mock_key_2": 5},
        {"mock_key_1": 2, "mock_key_2": 3},
    ]

    expected = (False, -1, "'data' is not valid under any of the given schemas")
    result = benchmark(yamltable.validate, dicts, schema_)
    actual = (result[0], result[1], result[2].split("\n")[0])
    assert actual == expected


@pytest.mark.unit
def test_validate_bad_data(
    schema: Schema, benchmark: bm.BenchmarkFixture
) -> None:
    """Check that validation works for unnested list of dictionaries."""

    dicts = [
        {"mock_key_1": 1, "mock_key_2": 5},
        {"mock_key_1": 2, "mock_key_2": False},
    ]

    expected = (False, 1, "False is not of type 'number'")
    result = benchmark(yamltable.validate, dicts, schema)
    actual = (result[0], result[1], result[2].split("\n")[0])
    assert actual == expected


@pytest.mark.unit
def test_validate_good_data(
    schema: Schema, benchmark: bm.BenchmarkFixture
) -> None:
    """Check that validation works for unnested list of dictionaries."""

    dicts = [
        {"mock_key_1": 1, "mock_key_2": 5},
        {"mock_key_1": 2, "mock_key_2": 3},
    ]

    expected = (True, -1, "")
    actual = benchmark(yamltable.validate, dicts, schema)
    assert actual == expected


@pytest.mark.unit
def test_yamltable_version() -> None:
    """Check that all the version tags are in sync."""

    # Check for pyproject.toml in two places in case of nonlocal install.
    toml_path = pathlib.Path("pyproject.toml")
    if toml_path.exists():
        pyproject_path = toml_path
    else:
        pyproject_path = pathlib.Path(yamltable.__file__).parents[2] / toml_path

    expected = toml.load(pyproject_path)["tool"]["poetry"]["version"]

    actual = yamltable.__version__
    assert actual == expected
