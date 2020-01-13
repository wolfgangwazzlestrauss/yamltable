"""Command line interface for YamlTable."""


import argparse
import pdb
import pprint

import yamltable


def main() -> None:
    """Command line interface for YamlTable."""

    parser = argparse.ArgumentParser(
        description="utilities for working with list organized YAML files"
    )
    parser.add_argument("-d", "--debug", action="store_true", help="run yamltable in debug mode")
    parser.add_argument("-v", "--version", action="version")
    subparser = parser.add_subparsers(dest="command", required=True)

    list_parser = subparser.add_parser(
        name="list", description="list dictionary key values", help="list dictionary key values"
    )
    list_parser.add_argument("key", type=str, help="dictionary key")
    list_parser.add_argument("file_path", type=str, help="YAML file location")

    search_parser = subparser.add_parser(
        name="search",
        description="search dictionaries by key and value",
        help="search dictionaries by key and value",
    )
    search_parser.add_argument("key", type=str, help="dictionary key")
    search_parser.add_argument("value", help="key value")
    search_parser.add_argument("file_path", type=str, help="YAML file location")

    sort_parser = subparser.add_parser(
        name="sort",
        description="sort dictionaries by key and value",
        help="sort dictionaries by key and value",
    )
    sort_parser.add_argument("key", type=str, help="dictionary key")
    sort_parser.add_argument("file_path", type=str, help="YAML file location")

    validate_parser = subparser.add_parser(
        name="validate", description="validate dictionaries", help="validate dictionaries"
    )
    validate_parser.add_argument("file_path", type=str, help="YAML file location")

    args = parser.parse_args()
    if args.debug:
        pdb.runcall(worker, args)
    else:
        worker(args)


def worker(args: argparse.Namespace) -> None:
    """Execute yamltable functionality

    :param args: command line arguments
    """

    try:
        dicts, schema = yamltable.read(args.file_path)
    except TypeError as xcpt:
        print(xcpt)
        return

    if args.command == "list":
        for dict_ in dicts:
            print(dict_[args.key])
    elif args.command == "search":
        for match in yamltable.search(args.key, args.value, dicts):
            pprint.pprint(match, indent=2)
    elif args.command == "sort":
        sorted_dicts = yamltable.sort(args.key, dicts)
        yamltable.write(args.file_path, sorted_dicts, schema)
    elif args.command == "validate":
        if schema is not None:
            yamltable.validate(dicts, schema)
        else:
            print("error: YAML file contains no schema")


if __name__ == "__main__":
    main()
