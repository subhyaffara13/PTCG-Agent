
def compress_cols(a):
    """
    Suppress whole columns of a 2-D array that contain masked values.

    This is equivalent to ``np.ma.compress_rowcols(a, 1)``, see
    `compress_rowcols` for details.

    Parameters
    ----------
    x : array_like, MaskedArray
        The array to operate on.  If not a MaskedArray instance (or if no array
        elements are masked), `x` is interpreted as a MaskedArray with
        `mask` set to `nomask`. Must be a 2D array.

    Returns
    -------
    compressed_array : ndarray
        The compressed array.

    See Also
    --------
    compress_rowcols

    Examples
    --------
    >>> import numpy as np
    >>> a = np.ma.array(np.arange(9).reshape(3, 3), mask=[[1, 0, 0],
    ...                                                   [1, 0, 0],
    ...                                                   [0, 0, 0]])
    >>> np.ma.compress_cols(a)
    array([[1, 2],
           [4, 5],
           [7, 8]])

    """
    a = asarray(a)
    if a.ndim != 2:
        raise NotImplementedError("compress_cols works for 2D arrays only.")
    return compress_rowcols(a, 1)

