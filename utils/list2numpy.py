
def list2numpy(l, dtype=object):  # pragma: no cover
    """Converts Python list of SymPy expressions to a NumPy array.

    See Also
    ========

    matrix2numpy
    """
    from numpy import empty
    a = empty(len(l), dtype)
    for i, s in enumerate(l):
        a[i] = s
    return a

