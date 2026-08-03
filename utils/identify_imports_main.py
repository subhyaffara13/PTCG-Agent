import sys

def identify_imports_main(
    argv: Sequence[str] | None = None, stdin: TextIOWrapper | None = None
) -> None:
    parser = argparse.ArgumentParser(
        description="Get all import definitions from a given file."
        "Use `-` as the first argument to represent stdin."
    )
    parser.add_argument(
        "files", nargs="+", help="One or more Python source files that need their imports sorted."
    )
    parser.add_argument(
        "--top-only",
        action="store_true",
        default=False,
        help="Only identify imports that occur in before functions or classes.",
    )

    target_group = parser.add_argument_group("target options")
    target_group.add_argument(
        "--follow-links",
        action="store_true",
        default=False,
        help="Tells isort to follow symlinks that are encountered when running recursively.",
    )

    uniqueness = parser.add_mutually_exclusive_group()
    uniqueness.add_argument(
        "--unique",
        action="store_true",
        default=False,
        help="If true, isort will only identify unique imports.",
    )
    uniqueness.add_argument(
        "--packages",
        dest="unique",
        action="store_const",
        const=api.ImportKey.PACKAGE,
        default=False,
        help="If true, isort will only identify the unique top level modules imported.",
    )
    uniqueness.add_argument(
        "--modules",
        dest="unique",
        action="store_const",
        const=api.ImportKey.MODULE,
        default=False,
        help="If true, isort will only identify the unique modules imported.",
    )
    uniqueness.add_argument(
        "--attributes",
        dest="unique",
        action="store_const",
        const=api.ImportKey.ATTRIBUTE,
        default=False,
        help="If true, isort will only identify the unique attributes imported.",
    )

    arguments = parser.parse_args(argv)

    file_names = arguments.files
    if file_names == ["-"]:
        identified_imports = api.find_imports_in_stream(
            sys.stdin if stdin is None else stdin,
            unique=arguments.unique,
            top_only=arguments.top_only,
            follow_links=arguments.follow_links,
        )
    else:
        identified_imports = api.find_imports_in_paths(
            file_names,
            unique=arguments.unique,
            top_only=arguments.top_only,
            follow_links=arguments.follow_links,
        )

    for identified_import in identified_imports:
        if arguments.unique == api.ImportKey.PACKAGE:
            print(identified_import.module.split(".")[0])
        elif arguments.unique == api.ImportKey.MODULE:
            print(identified_import.module)
        elif arguments.unique == api.ImportKey.ATTRIBUTE:
            print(f"{identified_import.module}.{identified_import.attribute}")
        else:
            print(str(identified_import))

