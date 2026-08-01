
def flatnotmasked_contiguous(a):
    """
    Find contiguous unmasked data in a masked array.

    Parameters
    ----------
    a : array_like
        The input array.

    Returns
    -------
    slice_list : list
        A sorted sequence of `slice` objects (start index, end index).

    See Also
    --------
    flatnotmasked_edges, notmasked_contiguous, notmasked_edges
    clump_masked, clump_unmasked

    Notes
    -----
    Only accepts 2-D arrays at most.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.ma.arange(10)
    >>> np.ma.flatnotmasked_contiguous(a)
    [slice(0, 10, None)]

    >>> mask = (a < 3) | (a > 8) | (a == 5)
    >>> a[mask] = np.ma.masked
    >>> np.array(a[~a.mask])
    array([3, 4, 6, 7, 8])

    >>> np.ma.flatnotmasked_contiguous(a)
    [slice(3, 5, None), slice(6, 9, None)]
    >>> a[:] = np.ma.masked
    >>> np.ma.flatnotmasked_contiguous(a)
    []

    """
    m = getmask(a)
    if m is nomask:
        return [slice(0, a.size)]
    i = 0
    result = []
    for (k, g) in itertools.groupby(m.ravel()):
        n = len(list(g))
        if not k:
            result.append(slice(i, i + n))
        i += n
    return result

