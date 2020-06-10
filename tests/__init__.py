"""Testing package for yamltable."""


import pathlib

import toml

import yamltable


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
