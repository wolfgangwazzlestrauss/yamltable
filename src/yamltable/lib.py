"""Library functions for YamlTable."""


import pprint
from typing import Any, Iterable, List, Optional, Tuple

import fastjsonschema
import yaml
from yamltable.typing import Path, Row, Schema


def read(file_path: Path) -> Tuple[List[Row], Optional[Schema]]:
    """Read data from YAML file.

    :param file_path: YAML file path
    :return: YAML data
    :raise TypeError: if file is not organized as a list
    """

    try:
        with open(file_path, "r") as handle:
            data = yaml.safe_load(handle)
    except (yaml.scanner.ScannerError, yaml.parser.ParserError) as xcpt:
        raise TypeError(f"invalid YAML file: {xcpt}")

    if isinstance(data, list):
        return data, None
    elif isinstance(data, dict):
        try:
            return data["rows"], data["schema"]
        except KeyError:
            raise TypeError("YAML file does not have a schema and rows organization")
    else:
        raise TypeError("YAML file is not organized in a tabular format")


def search(key: str, val: Any, rows: Iterable[Row]) -> List[Row]:
    """Search dictionaries by key and value.

    :param key: search key
    :param val: key comparison value
    :param rows: dictionaries to search
    :return: matching dictionaries
    """

    return [row for row in rows if key in row and row[key] == val]


def sort(key: str, rows: Iterable[Row]) -> List[Row]:
    """Sort dictionaries based on value for supplied key name.

    :param key: search key
    :param rows: dictionaries to sort
    :return: list of sorted dictionaries
    """

    return sorted(rows, key=lambda row: row[key])


def validate(rows: Iterable[Row], schema: Schema) -> None:
    """Check that each row satisfies the schema.

    :param rows:
    :param schema:
    :return:
    """

    try:
        validator = fastjsonschema.compile(schema)
    except fastjsonschema.JsonSchemaDefinitionException as xcpt:
        print(f"error: schema definition: {xcpt}")
        return

    for row in rows:
        try:
            validator(row)
        except fastjsonschema.JsonSchemaException as xcpt:
            print(xcpt)
            pprint.pprint(row, indent=2)


def write(
    file_path: Path, rows: List[Row], schema: Optional[Schema] = None, sort_keys: bool = False
) -> None:
    """Write data to YAML file.

    Additional sorts dictionary keys.

    :param file_path: YAML file path
    :param rows: list of dictionaries to write
    """

    if schema is None:
        with open(file_path, "w") as handle:
            yaml.dump(rows, handle, sort_keys=sort_keys)
    else:
        data = {"schema": schema, "rows": rows}
        with open(file_path, "w") as handle:
            yaml.dump(data, handle, sort_keys=sort_keys)
