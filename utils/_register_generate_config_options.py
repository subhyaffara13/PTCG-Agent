
def _register_generate_config_options(parser: argparse.ArgumentParser) -> None:
    """Registers the necessary arguments on the parser."""
    parser.prog = "pylint-config"
    # Overwrite the help command
    parser.add_argument(
        "-h",
        "--help",
        action=_HelpAction,
        default=argparse.SUPPRESS,
        help="show this help message and exit",
        parser=parser,
    )

    # We use subparsers to create various subcommands under 'pylint-config'
    subparsers = parser.add_subparsers(dest="config_subcommand", title="Subcommands")

    # Add the generate command
    generate_parser = subparsers.add_parser(
        "generate", help="Generate a pylint configuration"
    )
    generate_parser.add_argument("--interactive", action="store_true")

