
def handle_generate_command(linter: PyLinter) -> int:
    """Handle 'pylint-config generate'."""
    # Interactively generate a pylint configuration
    if linter.config.interactive:
        generate_interactive_config(linter)
        return 0
    print(get_subparser_help(linter, "generate"))
    return 32

