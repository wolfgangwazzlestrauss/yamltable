"""Command line interface for YamlTable."""


import pathlib

# import pdb  TODO: reimplement pdb support
import pprint
from typing import List, Optional, Tuple

import typer
import yamltable
from yamltable.typing import Row, Schema

app = typer.Typer()


@app.command()
def list(key: str, file_path: pathlib.Path) -> None:
    """List dictionary key values.

    Args:
        key: dictionary key
        file_path: YAML file location
    """

    rows, _ = load_data(file_path)
    for idx, row in enumerate(rows):
        try:
            typer.echo(row[key])
        except KeyError:
            typer.echo(f"error: row {idx} does not have key {key}")
            typer.Exit(1)


def load_data(file_path: pathlib.Path) -> Tuple[List[Row], Optional[Schema]]:
    """Attempt to load data from YAML file.

    Args:
        file_path: YAML file path

    Return:
        YAML row data, YAML schema
    """

    try:
        return yamltable.read(file_path)
    except (FileNotFoundError, TypeError) as xcpt:
        typer.echo(xcpt)
        raise typer.Exit(1)


@app.command()
def search(key: str, value: str, file_path: pathlib.Path) -> None:
    """Search dictionaries for matching key and value.

    Args:
        args: command line arguments
        rows: YAML file dictionaries
        schema: JSON schema for YAML file
    """

    rows, _ = load_data(file_path)
    for match in yamltable.search(key, value, rows):
        typer.echo(pprint.pformat(match, indent=2))


@app.command()
def sort(key: str, file_path: pathlib.Path) -> None:
    """Sort dictionaries by key values.

    Args:
        args: command line arguments
        rows: YAML file dictionaries
        schema: JSON schema for YAML file
    """

    rows, schema = load_data(file_path)
    try:
        sorted_rows = yamltable.sort(key, rows)
    except TypeError as xcpt:
        typer.echo(f"error: {xcpt}")
        typer.Exit(1)
    else:
        yamltable.write(file_path, sorted_rows, schema)


@app.command()
def validate(file_path: pathlib.Path) -> None:
    """Check that every dictionary has valid format.

    Args:
        args: command line arguments
        rows: YAML file dictionaries
        schema: JSON schema for YAML file
    """

    rows, schema = load_data(file_path)
    valid, row, msg = yamltable.validate(rows, schema)
    if valid:
        typer.echo("YAML file rows conform to its schema")
    elif row == -1:
        typer.echo(f"invalid schema: {msg}")
    else:
        typer.echo(f"invalid row {row}: {msg}")


if __name__ == "__main__":
    app()
