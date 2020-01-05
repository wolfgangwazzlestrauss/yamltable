"""Functional test functions from the yamltable module."""


import pathlib

import pytest
import yamltable


def test_sample(tmp_path: pathlib.Path) -> None:
    """Test sorting and overwriting file."""

    yaml_file = tmp_path / "file.yaml"
    yaml_file.write_text("- foo: 1\n  bar: 4\n- foo: 3\n  bar: 2\n")

    dicts = yamltable.read(yaml_file)
    sorted_dicts = yamltable.sort("bar", dicts)
    yamltable.write(yaml_file, sorted_dicts)

    expected = "- foo: 3\n  bar: 2\n- foo: 1\n  bar: 4\n"
    actual = yaml_file.read_text()
    assert actual == expected


if __name__ == "__main__":
    pytest.main()
