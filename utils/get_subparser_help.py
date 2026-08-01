
def get_subparser_help(linter: PyLinter, command: str) -> str:
    """Get the help message for one of the subcommands."""
    # Make sure subparsers are initialized properly
    assert linter._arg_parser._subparsers
    subparser_action = linter._arg_parser._subparsers._group_actions[0]
    assert isinstance(subparser_action, argparse._SubParsersAction)

    for name, subparser in subparser_action.choices.items():
        assert isinstance(subparser, argparse.ArgumentParser)
        if name == command:
            # Remove last character which is an extra new line
            return subparser.format_help()[:-1]
    return ""  # pragma: no cover

