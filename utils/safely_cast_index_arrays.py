
def safely_cast_index_arrays(A, idx_dtype=np.int32, msg=""):
    """Safely cast sparse array indices to `idx_dtype`.

    Check the shape of `A` to determine if it is safe to cast its index
    arrays to dtype `idx_dtype`. If any dimension in shape is larger than
    fits in the dtype, casting is unsafe so raise ``ValueError``.
    If safe, cast the index arrays to `idx_dtype` and return the result
    without changing the input `A`. The caller can assign results to `A`
    attributes if desired or use the recast index arrays directly.

    Unless downcasting is needed, the original index arrays are returned.
    You can test e.g. ``A.indptr is new_indptr`` to see if downcasting occurred.

    .. versionadded:: 1.15.0

    Parameters
    ----------
    A : sparse array or matrix
        The array for which index arrays should be downcast.
    idx_dtype : dtype
        Desired dtype. Should be an integer dtype (default: ``np.int32``).
        Most of scipy.sparse uses either int64 or int32.
    msg : str, optional
        A string to be added to the end of the ValueError message
        if the array shape is too big to fit in `idx_dtype`.
        The error message is ``f"<index> values too large for {msg}"``
        It should indicate why the downcasting is needed, e.g. "SuperLU",
        and defaults to f"dtype {idx_dtype}".

    Returns
    -------
    idx_arrays : ndarray or tuple of ndarrays
        Based on ``A.format``, index arrays are returned after casting to `idx_dtype`.
        For CSC/CSR, returns ``(indices, indptr)``.
        For COO, returns ``coords``.
        For DIA, returns ``offsets``.
        For BSR, returns ``(indices, indptr)``.

    Raises
    ------
    ValueError
        If the array has shape that would not fit in the new dtype, or if
        the sparse format does not use index arrays.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import sparse
    >>> data = [3]
    >>> coords = (np.array([3]), np.array([1]))  # Note: int64 arrays
    >>> A = sparse.coo_array((data, coords))
    >>> A.coords[0].dtype
    dtype('int64')

    >>> # rescast after construction, raising exception if shape too big
    >>> coords = sparse.safely_cast_index_arrays(A, np.int32)
    >>> A.coords[0] is coords[0]  # False if casting is needed
    False
    >>> A.coords = coords  # set the index dtype of A
    >>> A.coords[0].dtype
    dtype('int32')
    """
    if not msg:
        msg = f"dtype {idx_dtype}"
    # check for safe downcasting
    max_value = np.iinfo(idx_dtype).max

    if A.format in ("csc", "csr"):
        # indptr[-1] is max b/c indptr always sorted
        if A.indptr[-1] > max_value:
            raise ValueError(f"indptr values too large for {msg}")

        # check shape vs dtype
        if max(*A.shape) > max_value:
            if (A.indices > max_value).any():
                raise ValueError(f"indices values too large for {msg}")

        indices = A.indices.astype(idx_dtype, copy=False)
        indptr = A.indptr.astype(idx_dtype, copy=False)
        return indices, indptr

    elif A.format == "coo":
        if max(*A.shape) > max_value:
            if any((co > max_value).any() for co in A.coords):
                raise ValueError(f"coords values too large for {msg}")
        return tuple(co.astype(idx_dtype, copy=False) for co in A.coords)

    elif A.format == "dia":
        if max(*A.shape) > max_value:
            if (A.offsets > max_value).any():
                raise ValueError(f"offsets values too large for {msg}")
        offsets = A.offsets.astype(idx_dtype, copy=False)
        return offsets

    elif A.format == 'bsr':
        R, C = A.blocksize
        if A.indptr[-1] * R > max_value:
            raise ValueError("indptr values too large for {msg}")
        if max(*A.shape) > max_value:
            if (A.indices * C > max_value).any():
                raise ValueError(f"indices values too large for {msg}")
        indices = A.indices.astype(idx_dtype, copy=False)
        indptr = A.indptr.astype(idx_dtype, copy=False)
        return indices, indptr

    else:
        raise TypeError(f'Format {A.format} is not associated with index arrays. '
                        'DOK and LIL have dict and list, not array.')

