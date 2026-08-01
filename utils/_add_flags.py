
def _add_flags(value: str, type: str) -> str:
    """
    Add any flags from the environment for the given type.

    type is the prefix to FLAGS in the environment key (e.g. "C" for "CFLAGS").
    """
    flags = os.environ.get(f'{type}FLAGS')
    return f'{value} {flags}' if flags else value

