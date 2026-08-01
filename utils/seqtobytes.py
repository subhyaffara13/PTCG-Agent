
def seqtobytes(s):
    """Convert a sequence of integers to a *bytes* instance.  Good for
    plastering over Python 2 / Python 3 cracks.
    """

    return strtobytes("".join(chr(x) for x in s))

