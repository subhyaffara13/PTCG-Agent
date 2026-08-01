
def set_min_indent(docstring: str, indent_level: int) -> str:
    """
    Adjust the indentation of a docstring to match the specified indent level.
    """
    # Equivalent to textwrap.dedent + textwrap.indent but avoids the two regex
    # passes that textwrap uses internally (one per call in dedent, one in indent).
    lines = docstring.split("\n")
    min_indent = min(
        (len(line) - len(line.lstrip()) for line in lines if line.strip()),
        default=0,
    )
    prefix = " " * indent_level
    return "\n".join(prefix + line[min_indent:] if line.strip() else "" for line in lines)

