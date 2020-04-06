"""Reusable testing fixtures for YamlTable."""


import pathlib

import pytest

import yamltable


@pytest.fixture
def tmp_yaml(tmp_path: pathlib.Path) -> pathlib.Path:
    """Temporary copy of path.yaml."""
    repo_path = pathlib.Path(yamltable.__file__).parents[2]

    dest_path = tmp_path / "path.yaml"
    src_path = repo_path / "tests/data/path.yaml"

    text = src_path.read_text()
    dest_path.write_text(text)

    return dest_path
