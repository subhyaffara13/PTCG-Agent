
def uncomment_line(line, prefix, suffix=""):
    """Remove prefix (and space) from line"""
    if prefix:
        if line.startswith(prefix + " "):
            line = line[len(prefix) + 1 :]
        elif line.startswith(prefix):
            line = line[len(prefix) :]
    if suffix:
        if line.endswith(suffix + " "):
            line = line[: -(1 + len(suffix))]
        elif line.endswith(suffix):
            line = line[: -len(suffix)]
    return line

