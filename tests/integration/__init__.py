"""Integration tests for the yamltable library."""


import pathlib

import yamltable


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