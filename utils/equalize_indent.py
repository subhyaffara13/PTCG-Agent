
def equalize_indent(docstring: str, indent_level: int) -> str:
    """
    Adjust the indentation of a docstring to match the specified indent level.
    """
    prefix = " " * indent_level
    # Uses splitlines() (no keepends) to match previous behaviour that dropped
    # any trailing newline via the old splitlines() + "\n".join() + textwrap.indent path.
    return "\n".join(prefix + line.lstrip() if line.strip() else "" for line in docstring.splitlines())

