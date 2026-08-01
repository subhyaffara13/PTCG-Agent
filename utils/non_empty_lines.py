
def non_empty_lines(path):
    """
    Yield non-empty lines from file at path
    """
    for line in _read_utf8_with_fallback(path).splitlines():
        line = line.strip()
        if line:
            yield line

