"""Script for interacting with profiling utilities."""


import enum
import pathlib
import subprocess
import webbrowser

import typer


app = typer.Typer(help=__doc__)


class Format(enum.Enum):
    """Profiling results format."""

    FLAMEGRAPH = "flamegraph"
    SPEEDSCOPE = "speedscope"


def run_command(command: str, error_msg: str) -> None:
    """Run shell command and print error message on failure.

    Args:
        command: Command to execute after preparing documentation.
        error_msg: Error message if command fails.
    """
    try:
        subprocess.run(args=command, shell=True, check=True)
    except subprocess.CalledProcessError:
        typer.secho(f"Error: {error_msg}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


def _launch(prof_path: pathlib.Path, fmt: Format) -> None:
    """Open profiler output in web browser."""
    if fmt == Format.SPEEDSCOPE:
        run_command(
            f"npm run profile -- {prof_path}",
            "Error: Unable to run speedscope.",
        )
    else:
        webbrowser.open(prof_path.absolute().as_uri())


def _prof_path(fmt: Format) -> pathlib.Path:
    """Get profile results output path.

    Creates the results parent directory if it does not exist.

    Args:
        fmt: Profiler results output format.

    Returns:
        Profiler results output path.
    """
    prof_dir = pathlib.Path("scripts/.cache/profile")
    if fmt == Format.SPEEDSCOPE:
        prof_file = "speedscope.json"
    else:
        prof_file = "flamegraph.svg"

    prof_dir.mkdir(parents=True, exist_ok=True)
    return prof_dir / prof_file


@app.command()
def profile(
    launch: bool = typer.Option(
        True, help="Show profile results in web browser."
    ),
    fmt: Format = typer.Option(
        Format.SPEEDSCOPE.value, help="Profile results output format."
    ),
) -> None:
    """Profile Python code with py-spy."""
    prof_path = _prof_path(fmt)

    pyspy = "py-spy record --format speedscope"
    prog = "yamltable search name drive tests/data/path.yaml"
    command = f"{pyspy} -o {prof_path} -- {prog}"

    run_command(command, "Error: Unable to execute profiler.")
    if launch:
        _launch(prof_path, fmt)


if __name__ == "__main__":
    app()
