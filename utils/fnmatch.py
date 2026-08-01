
def fnmatch(filename: str, patterns: Sequence[str]) -> bool:
    """Wrap :func:`fnmatch.fnmatch` to add some functionality.

    :param filename:
        Name of the file we're trying to match.
    :param patterns:
        Patterns we're using to try to match the filename.
    :param default:
        The default value if patterns is empty
    :returns:
        True if a pattern matches the filename, False if it doesn't.
        ``True`` if patterns is empty.
    """
    if not patterns:
        return True
    return any(_fnmatch.fnmatch(filename, pattern) for pattern in patterns)

