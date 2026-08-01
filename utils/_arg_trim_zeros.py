
def _arg_trim_zeros(filt):
    """Return indices of the first and last non-zero element.

    Parameters
    ----------
    filt : array_like
        Input array.

    Returns
    -------
    start, stop : ndarray
        Two arrays containing the indices of the first and last non-zero
        element in each dimension.

    See also
    --------
    trim_zeros

    Examples
    --------
    >>> import numpy as np
    >>> _arg_trim_zeros(np.array([0, 0, 1, 1, 0]))
    (array([2]), array([3]))
    """
    nonzero = (
        np.argwhere(filt)
        if filt.dtype != np.object_
        # Historically, `trim_zeros` treats `None` in an object array
        # as non-zero while argwhere doesn't, account for that
        else np.argwhere(filt != 0)
    )
    if nonzero.size == 0:
        start = stop = np.array([], dtype=np.intp)
    else:
        start = nonzero.min(axis=0)
        stop = nonzero.max(axis=0)
    return start, stop

