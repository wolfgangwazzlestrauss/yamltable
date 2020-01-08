"""Unit test functions from the yamltable module."""


from unittest import mock

import pytest
import yamltable


@pytest.mark.parametrize(
    "file_data", ["mock_key_1: 1\nmock_key_2: 5", "mock_key_1: 1\n- mock_key_2: 5"]
)
def test_read_bad_data(file_data: str) -> None:
    """Check that reader throws an exception when reading invalid YAML file."""

    with mock.patch("builtins.open", mock.mock_open(read_data=file_data)):
        with pytest.raises(TypeError):
            yamltable.read("mock_file_path.yaml")


def test_read_good_data() -> None:
    """Check that reader correctly reads data that is a list."""

    file_data = "- mock_key: 1\n- mock_key: 5"

    expected = [{"mock_key": 1}, {"mock_key": 5}]
    with mock.patch("builtins.open", mock.mock_open(read_data=file_data)):
        actual, _ = yamltable.read("mock_file_path.yaml")

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


if __name__ == "__main__":
    pytest.main()
