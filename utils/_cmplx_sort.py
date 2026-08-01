
def _cmplx_sort(p):
    """Sort roots based on magnitude.

    Parameters
    ----------
    p : array_like
        The roots to sort, as a 1-D array.

    Returns
    -------
    p_sorted : ndarray
        Sorted roots.
    indx : ndarray
        Array of indices needed to sort the input `p`.

    Examples
    --------
    >>> from scipy.signal._signaltools import _cmplx_sort
    >>> vals = [1, 4, 1+1.j, 3]
    >>> p_sorted, indx = _cmplx_sort(vals)
    >>> p_sorted
    array([1.+0.j, 1.+1.j, 3.+0.j, 4.+0.j])
    >>> indx
    array([0, 2, 3, 1])
    """
    p = np.asarray(p)
    indx = np.argsort(abs(p))
    return np.take(p, indx, 0), indx

