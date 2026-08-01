
def jupyter_parser() -> JupyterParser:
    """Create a jupyter parser object."""
    parser = JupyterParser(
        description="Jupyter: Interactive Computing",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    # don't use argparse's version action because it prints to stderr on py2
    group.add_argument(
        "--version", action="store_true", help="show the versions of core jupyter packages and exit"
    )
    subcommand_action = group.add_argument(
        "subcommand", type=str, nargs="?", help="the subcommand to launch"
    )
    # For argcomplete, supply all known subcommands
    subcommand_action.completer = lambda *args, **kwargs: list_subcommands()  # type: ignore[attr-defined]  # noqa: ARG005

    group.add_argument("--config-dir", action="store_true", help="show Jupyter config dir")
    group.add_argument("--data-dir", action="store_true", help="show Jupyter data dir")
    group.add_argument("--runtime-dir", action="store_true", help="show Jupyter runtime dir")
    group.add_argument(
        "--paths",
        action="store_true",
        help="show all Jupyter paths. Add --json for machine-readable format.",
    )
    parser.add_argument("--json", action="store_true", help="output paths as machine-readable json")
    parser.add_argument("--debug", action="store_true", help="output debug information about paths")

    return parser

