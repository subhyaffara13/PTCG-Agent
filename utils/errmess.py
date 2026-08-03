import sys

def errmess(s: str) -> None:
    """
    Write an error message to stderr.

    This indirection is needed because sys.stderr might not always be available (see #26862).
    """
    if sys.stderr is not None:
        sys.stderr.write(s)

