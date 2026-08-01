
def filename_match(filename, patterns, default=True):
    """Check if patterns contains a pattern that matches filename.

    If patterns is unspecified, this always returns True.
    """
    if not patterns:
        return default
    return any(fnmatch(filename, pattern) for pattern in patterns)

