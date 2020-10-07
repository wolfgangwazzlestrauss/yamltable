"""Reusable testing fixtures for YamlTable."""


import pathlib

import pytest


@pytest.fixture
def tmp_yaml(tmp_path: pathlib.Path) -> pathlib.Path:
    """Temporary copy of path.yaml."""

    dest_path = tmp_path / "path.yaml"
    src_path = pathlib.Path("tests/data/path.yaml")

    text = src_path.read_text()
    dest_path.write_text(text)

    return dest_path
