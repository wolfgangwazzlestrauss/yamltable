"""Copy index file and build documentation."""


import pathlib
import shutil
import subprocess
import sys


def build_docs() -> None:
    """Build documentation with MkDocs."""

    try:
        subprocess.run(args="mkdocs build", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Failed to build project documentation.", sys.stderr)
        sys.exit(1)


def copy_index() -> None:
    """Sync documentation index with repository README file."""

    repo_path = pathlib.Path(__file__).parents[1]

    src_path = repo_path / "docs/index.md"
    dest_path = repo_path / "README.md"

    shutil.copy(src=src_path, dst=dest_path)


def main() -> None:
    """Entrypoint for documentation building."""

    copy_index()
    build_docs()


if __name__ == "__main__":
    main()
