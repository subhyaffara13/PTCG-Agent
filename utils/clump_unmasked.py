
def clump_unmasked(a):
    """
    Return list of slices corresponding to the unmasked clumps of a 1-D array.
    (A "clump" is defined as a contiguous region of the array).

    Parameters
    ----------
    a : ndarray
        A one-dimensional masked array.

    Returns
    -------
    slices : list of slice
        The list of slices, one for each continuous region of unmasked
        elements in `a`.

    See Also
    --------
    flatnotmasked_edges, flatnotmasked_contiguous, notmasked_edges
    notmasked_contiguous, clump_masked

    Examples
    --------
    >>> import numpy as np
    >>> a = np.ma.masked_array(np.arange(10))
    >>> a[[0, 1, 2, 6, 8, 9]] = np.ma.masked
    >>> np.ma.clump_unmasked(a)
    [slice(3, 6, None), slice(7, 8, None)]

    """
    mask = getattr(a, '_mask', nomask)
    if mask is nomask:
        return [slice(0, a.size)]
    return _ezclump(~mask)

