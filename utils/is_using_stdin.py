
def is_using_stdin(paths: list[str]) -> bool:
    """Determine if we're going to read from stdin.

    :param paths:
        The paths that we're going to check.
    :returns:
        True if stdin (-) is in the path, otherwise False
    """
    return "-" in paths

