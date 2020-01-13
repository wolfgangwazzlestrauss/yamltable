"""Integration tests for YamlTable's command line interface."""


import pathlib

import pytest
import toml
import yamltable


def test_version() -> None:
    """Check that the two version tags are in sync."""

    pyproject_path = pathlib.Path(yamltable.__file__).parents[2] / "pyproject.toml"
    expected = toml.load(pyproject_path)["tool"]["poetry"]["version"]

    actual = yamltable.__version__
    assert actual == expected


if __name__ == "__main__":
    pytest.main()
