
def _enum_help(msg: str, e: type[enum.Enum]) -> str:  # pragma: no cover
    """
    Render a `--help`-style string for the given enumeration.
    """
    return f"{msg} (choices: {', '.join(str(v) for v in e)})"

