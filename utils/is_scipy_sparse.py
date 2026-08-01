
def is_scipy_sparse(arr) -> bool:
    """
    Check whether an array-like is a scipy.sparse.spmatrix instance.

    Parameters
    ----------
    arr : array-like
        The array-like to check.

    Returns
    -------
    boolean
        Whether or not the array-like is a scipy.sparse.spmatrix instance.

    Notes
    -----
    If scipy is not installed, this function will always return False.

    Examples
    --------
    >>> from scipy.sparse import bsr_matrix
    >>> is_scipy_sparse(bsr_matrix([1, 2, 3]))
    True
    >>> is_scipy_sparse(pd.arrays.SparseArray([1, 2, 3]))
    False
    """
    global _is_scipy_sparse

    if _is_scipy_sparse is None:
        try:
            from scipy.sparse import issparse as _is_scipy_sparse
        except ImportError:
            _is_scipy_sparse = lambda _: False

    assert _is_scipy_sparse is not None
    return _is_scipy_sparse(arr)

