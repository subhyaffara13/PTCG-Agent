
def is_sparse(A):
    """Check if tensor A is a sparse COO tensor. All other sparse storage formats (CSR, CSC, etc...) will return False."""
    if isinstance(A, torch.Tensor):
        return A.layout == torch.sparse_coo

    error_str = "expected Tensor"
    if not torch.jit.is_scripting():
        error_str += f" but got {type(A)}"
    raise TypeError(error_str)


def is_sparse(arr) -> bool:
    """
    Check whether an array-like is a 1-D pandas sparse array.

    .. deprecated:: 2.1.0
        Use isinstance(dtype, pd.SparseDtype) instead.

    Check that the one-dimensional array-like is a pandas sparse array.
    Returns True if it is a pandas sparse array, not another type of
    sparse array.

    Parameters
    ----------
    arr : array-like
        Array-like to check.

    Returns
    -------
    bool
        Whether or not the array-like is a pandas sparse array.

    See Also
    --------
    api.types.SparseDtype : The dtype object for pandas sparse arrays.

    Examples
    --------
    Returns `True` if the parameter is a 1-D pandas sparse array.

    >>> from pandas.api.types import is_sparse
    >>> is_sparse(pd.arrays.SparseArray([0, 0, 1, 0]))
    True
    >>> is_sparse(pd.Series(pd.arrays.SparseArray([0, 0, 1, 0])))
    True

    Returns `False` if the parameter is not sparse.

    >>> is_sparse(np.array([0, 0, 1, 0]))
    False
    >>> is_sparse(pd.Series([0, 1, 0, 0]))
    False

    Returns `False` if the parameter is not a pandas sparse array.

    >>> from scipy.sparse import bsr_matrix
    >>> is_sparse(bsr_matrix([0, 1, 0, 0]))
    False

    Returns `False` if the parameter has more than one dimension.
    """
    warnings.warn(
        "is_sparse is deprecated and will be removed in a future "
        "version. Check `isinstance(dtype, pd.SparseDtype)` instead.",
        Pandas4Warning,
        stacklevel=2,
    )

    dtype = getattr(arr, "dtype", arr)
    return isinstance(dtype, SparseDtype)


def is_sparse(x):
  return isinstance(x, sparse.JAXSparse)

