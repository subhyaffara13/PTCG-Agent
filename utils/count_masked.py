
def count_masked(arr, axis=None):
    """
    Count the number of masked elements along the given axis.

    Parameters
    ----------
    arr : array_like
        An array with (possibly) masked elements.
    axis : int, optional
        Axis along which to count. If None (default), a flattened
        version of the array is used.

    Returns
    -------
    count : int, ndarray
        The total number of masked elements (axis=None) or the number
        of masked elements along each slice of the given axis.

    See Also
    --------
    MaskedArray.count : Count non-masked elements.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(9).reshape((3,3))
    >>> a = np.ma.array(a)
    >>> a[1, 0] = np.ma.masked
    >>> a[1, 2] = np.ma.masked
    >>> a[2, 1] = np.ma.masked
    >>> a
    masked_array(
      data=[[0, 1, 2],
            [--, 4, --],
            [6, --, 8]],
      mask=[[False, False, False],
            [ True, False,  True],
            [False,  True, False]],
      fill_value=999999)
    >>> np.ma.count_masked(a)
    3

    When the `axis` keyword is used an array is returned.

    >>> np.ma.count_masked(a, axis=0)
    array([1, 1, 1])
    >>> np.ma.count_masked(a, axis=1)
    array([0, 2, 1])

    """
    m = getmaskarray(arr)
    return m.sum(axis)

