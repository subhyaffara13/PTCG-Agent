
def cleanupBox(box):
    """Return a sparse copy of `box`, without redundant (default) values.

    >>> cleanupBox({})
    {}
    >>> cleanupBox({'wdth': (0.0, 1.0)})
    {'wdth': (0.0, 1.0)}
    >>> cleanupBox({'wdth': (-1.0, 1.0)})
    {}

    """
    return {tag: limit for tag, limit in box.items() if limit != (-1.0, 1.0)}

