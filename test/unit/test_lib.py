"""Unit test functions from the yamltable module."""


import unittest
from unittest import mock

import pytest
import yamltable


class TestSearch(unittest.TestCase):
    """Tests for searching lists of dictionaries by key and value."""

    def test_search(self) -> None:
        """Check that searching works for unnested list of dictionaries."""

        dicts = [{"mock_key_1": 1, "mock_key_2": 5}, {"mock_key_1": 2, "mock_key_2": 3}]

        expected = [{"mock_key_1": 2, "mock_key_2": 3}]
        actual = yamltable.search("mock_key_2", 3, dicts)
        self.assertEqual(actual, expected)


class TestSort(unittest.TestCase):
    """Tests for sorting lists of dictionaries by key."""

    def test_sort(self) -> None:
        """Check that sorting works for unnested list of dictionaries."""

        dicts = [{"mock_key_1": 1, "mock_key_2": 5}, {"mock_key_1": 2, "mock_key_2": 3}]

        expected = [{"mock_key_1": 2, "mock_key_2": 3}, {"mock_key_1": 1, "mock_key_2": 5}]
        actual = yamltable.sort("mock_key_2", dicts)
        self.assertEqual(actual, expected)


class TestRead(unittest.TestCase):
    """Tests for reading YAML files."""

    def test_read_bad_data(self) -> None:
        """Check that reader throws an exception when loading data that is not a list."""

        file_data = "mock_key_1: 1\nmock_key_2: 5"

        with mock.patch("builtins.open", mock.mock_open(read_data=file_data)):
            with self.assertRaises(TypeError):
                yamltable.read("mock_file_path.yaml")

    def test_read_good_data(self) -> None:
        """Check that reader correctly reads data that is a list."""

        file_data = "- mock_key: 1\n- mock_key: 5"

        expected = [{"mock_key": 1}, {"mock_key": 5}]
        with mock.patch("builtins.open", mock.mock_open(read_data=file_data)):
            actual, _ = yamltable.read("mock_file_path.yaml")
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    pytest.main()
