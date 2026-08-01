
def _get_global_options_documentation(linter: PyLinter) -> str:
    """Get documentation for the main checker."""
    result = get_rst_title("Pylint global options and switches", "-")
    result += """
Pylint provides global options and switches.

"""
    for checker in linter.get_checkers():
        if checker.name == MAIN_CHECKER_NAME and checker.options:
            for section, options in checker._options_by_section():
                if section is None:
                    title = "General options"
                else:
                    title = f"{section.capitalize()} options"
                result += get_rst_title(title, "~")
                assert isinstance(options, list)
                result += f"{get_rst_section(None, options)}\n"
    return result

