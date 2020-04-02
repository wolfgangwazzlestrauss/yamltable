"""Script for building images and running containers with Docker."""


import subprocess

import typer

import yamltable


app = typer.Typer(
    help="Script for building images and running containers with Docker."
)


@app.command()
def build() -> None:
    """Build image from project Dockerfile."""

    tag = yamltable.__version__
    command = f"docker build -t wolfgangwazzlestrauss/yamltable:{tag} ."
    error_msg = "Failed to build Docker image."
    run_command(command, error_msg)


@app.command()
def prune() -> None:
    """Prune all containers and images on system."""

    error_msg = "Failed to prune system {}."
    run_command("docker container prune -f", error_msg.format("containers"))
    run_command("docker image prune -f", error_msg.format("images"))


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


@app.command()
def run(
    build: bool = typer.Option(False, help="Build image before running.")
) -> None:
    """Run project Docker image."""

    tag = yamltable.__version__
    image = f"wolfgangwazzlestrauss/yamltable:{tag}"

    command = f"docker run -it --rm --name yamltable {image}"
    error_msg = "Failed to run Docker container."
    run_command(command, error_msg)


if __name__ == "__main__":
    app()
