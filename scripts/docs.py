"""Copies and generates files for docs folder and builds documentation."""


from pathlib import Path
import shutil
import subprocess
import sys


def build_docs() -> None:
    """Build documentation with MkDocs."""

    try:
        subprocess.run(args="mkdocs build --strict", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Failed to build project documentation.", sys.stderr)
        sys.exit(1)


def copy_files(repo_path: Path) -> None:
    """Copy repository files into docs folder.

    Args:
        repo_path: Repository root path.
    """

    paths = [
        ("CHANGELOG.md", "docs/changelog.md"),
        ("LICENSE.md", "docs/license.md"),
        ("README.md", "docs/index.md"),
    ]

    for src, dest in paths:
        shutil.copy(src=repo_path / src, dst=repo_path / dest)


def generate_cli_docs(repo_path: Path) -> None:
    """Create documentation for the command line interface.

    Args:
        repo_path: Repository root path.
    """

    cli_doc = repo_path / "docs/api/cli.md"

    with cli_doc.open("w") as handle:
        try:
            subprocess.run(
                args="typer src/yamltable/__main__.py utils docs",
                shell=True,
                check=True,
                stdout=handle,
            )
        except subprocess.CalledProcessError:
            print(
                "Failed to build command line interface documentation.",
                sys.stderr,
            )
            sys.exit(1)


def main() -> None:
    """Entrypoint for documentation building."""

    repo_path = Path(__file__).parents[1]
    copy_files(repo_path)
    generate_cli_docs(repo_path)
    build_docs()


if __name__ == "__main__":
    main()
