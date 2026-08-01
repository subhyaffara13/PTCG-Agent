
def mask_rowcols(a, axis=None):
    """
    Mask rows and/or columns of a 2D array that contain masked values.

    Mask whole rows and/or columns of a 2D array that contain
    masked values.  The masking behavior is selected using the
    `axis` parameter.

      - If `axis` is None, rows *and* columns are masked.
      - If `axis` is 0, only rows are masked.
      - If `axis` is 1 or -1, only columns are masked.

    Parameters
    ----------
    a : array_like, MaskedArray
        The array to mask.  If not a MaskedArray instance (or if no array
        elements are masked), the result is a MaskedArray with `mask` set
        to `nomask` (False). Must be a 2D array.
    axis : int, optional
        Axis along which to perform the operation. If None, applies to a
        flattened version of the array.

    Returns
    -------
    a : MaskedArray
        A modified version of the input array, masked depending on the value
        of the `axis` parameter.

    Raises
    ------
    NotImplementedError
        If input array `a` is not 2D.

    See Also
    --------
    mask_rows : Mask rows of a 2D array that contain masked values.
    mask_cols : Mask cols of a 2D array that contain masked values.
    masked_where : Mask where a condition is met.

    Notes
    -----
    The input array's mask is modified by this function.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.zeros((3, 3), dtype=np.int_)
    >>> a[1, 1] = 1
    >>> a
    array([[0, 0, 0],
           [0, 1, 0],
           [0, 0, 0]])
    >>> a = np.ma.masked_equal(a, 1)
    >>> a
    masked_array(
      data=[[0, 0, 0],
            [0, --, 0],
            [0, 0, 0]],
      mask=[[False, False, False],
            [False,  True, False],
            [False, False, False]],
      fill_value=1)
    >>> np.ma.mask_rowcols(a)
    masked_array(
      data=[[0, --, 0],
            [--, --, --],
            [0, --, 0]],
      mask=[[False,  True, False],
            [ True,  True,  True],
            [False,  True, False]],
      fill_value=1)

    """
    a = array(a, subok=False)
    if a.ndim != 2:
        raise NotImplementedError("mask_rowcols works for 2D arrays only.")
    m = getmask(a)
    # Nothing is masked: return a
    if m is nomask or not m.any():
        return a
    maskedval = m.nonzero()
    a._mask = a._mask.copy()
    if not axis:
        a[np.unique(maskedval[0])] = masked
    if axis in [None, 1, -1]:
        a[:, np.unique(maskedval[1])] = masked
    return a

