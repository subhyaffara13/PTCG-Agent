
def _handle_pylint_config_commands(linter: PyLinter) -> int:
    """Handle whichever command is passed to 'pylint-config'."""
    if linter.config.config_subcommand == "generate":
        return handle_generate_command(linter)

    print(get_help(linter._arg_parser))
    return 32

