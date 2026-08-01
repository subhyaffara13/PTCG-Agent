
def _get_checkers_documentation(linter: PyLinter, show_options: bool = True) -> str:
    """Get documentation for individual checkers."""
    if show_options:
        result = _get_global_options_documentation(linter)
    else:
        result = ""

    result += get_rst_title("Pylint checkers' options and switches", "-")
    result += """\

Pylint checkers can provide three set of features:

* options that control their execution,
* messages that they can raise,
* reports that they can generate.

Below is a list of all checkers and their features.

"""
    by_checker = _get_checkers_infos(linter)
    for checker_name in sorted(by_checker):
        information = by_checker[checker_name]
        checker = information["checker"]
        del information["checker"]
        result += checker.get_full_documentation(
            **information, show_options=show_options
        )
    return result

