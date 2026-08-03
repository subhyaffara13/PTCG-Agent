import sys

def print_full_documentation(
    linter: PyLinter, stream: TextIO = sys.stdout, show_options: bool = True
) -> None:
    """Output a full documentation in ReST format."""
    print(
        _get_checkers_documentation(linter, show_options=show_options)[:-3], file=stream
    )

