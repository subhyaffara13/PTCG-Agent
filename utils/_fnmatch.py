
def _fnmatch(filepath, patterns):
    return any(fnmatch.fnmatch(filepath, pattern) for pattern in patterns)

