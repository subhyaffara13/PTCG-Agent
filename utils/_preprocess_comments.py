
def _preprocess_comments(iterable, comments, encoding):
    """
    Generator that consumes a line iterated iterable and strips out the
    multiple (or multi-character) comments from lines.
    This is a pre-processing step to achieve feature parity with loadtxt
    (we assume that this feature is a niche feature).
    """
    for line in iterable:
        if isinstance(line, bytes):
            # Need to handle conversion here, or the splitting would fail
            line = line.decode(encoding)

        for c in comments:
            line = line.split(c, 1)[0]

        yield line

