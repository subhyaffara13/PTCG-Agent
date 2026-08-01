
def clump_masked(a):
    """
    Returns a list of slices corresponding to the masked clumps of a 1-D array.
    (A "clump" is defined as a contiguous region of the array).

    Parameters
    ----------
    a : ndarray
        A one-dimensional masked array.

    Returns
    -------
    slices : list of slice
        The list of slices, one for each continuous region of masked elements
        in `a`.

    See Also
    --------
    flatnotmasked_edges, flatnotmasked_contiguous, notmasked_edges
    notmasked_contiguous, clump_unmasked

    Examples
    --------
    >>> import numpy as np
    >>> a = np.ma.masked_array(np.arange(10))
    >>> a[[0, 1, 2, 6, 8, 9]] = np.ma.masked
    >>> np.ma.clump_masked(a)
    [slice(0, 3, None), slice(6, 7, None), slice(8, 10, None)]

    """
    mask = ma.getmask(a)
    if mask is nomask:
        return []
    return _ezclump(mask)

