
def spsolve_triangular(A, b, lower=True, overwrite_A=False, overwrite_b=False,
                       unit_diagonal=False):
    """
    Solve the equation ``A x = b`` for `x`, assuming A is a triangular matrix.

    Parameters
    ----------
    A : (M, M) sparse array or matrix
        A sparse square triangular matrix. Should be in CSR or CSC format.
    b : (M,) or (M, N) array_like
        Right-hand side matrix in ``A x = b``
    lower : bool, optional
        Whether `A` is a lower or upper triangular matrix.
        Default is lower triangular matrix.
    overwrite_A : bool, optional
        Allow changing `A`.
        Enabling gives a performance gain. Default is False.
    overwrite_b : bool, optional
        Allow overwriting data in `b`.
        Enabling gives a performance gain. Default is False.
        If `overwrite_b` is True, it should be ensured that
        `b` has an appropriate dtype to be able to store the result.
    unit_diagonal : bool, optional
        If True, diagonal elements of `a` are assumed to be 1.

        .. versionadded:: 1.4.0

    Returns
    -------
    x : (M,) or (M, N) ndarray
        Solution to the system ``A x = b``. Shape of return matches shape
        of `b`.

    Raises
    ------
    LinAlgError
        If `A` is singular or not triangular.
    ValueError
        If shape of `A` or shape of `b` do not match the requirements.

    Notes
    -----
    .. versionadded:: 0.19.0

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csc_array
    >>> from scipy.sparse.linalg import spsolve_triangular
    >>> A = csc_array([[3, 0, 0], [1, -1, 0], [2, 0, 1]], dtype=float)
    >>> B = np.array([[2, 0], [-1, 0], [2, 0]], dtype=float)
    >>> x = spsolve_triangular(A, B)
    >>> np.allclose(A.dot(x), B)
    True
    """

    if is_pydata_spmatrix(A):
        A = A.to_scipy_sparse().tocsc()

    trans = "N"
    if issparse(A) and A.format == "csr":
        A = A.T
        trans = "T"
        lower = not lower

    if not (issparse(A) and A.format == "csc"):
        warn('CSC or CSR matrix format is required. Converting to CSC matrix.',
             SparseEfficiencyWarning, stacklevel=2)
        A = csc_array(A)
    elif not overwrite_A:
        A = A.copy()


    M, N = A.shape
    if M != N:
        raise ValueError(
            f'A must be a square matrix but its shape is {A.shape}.')

    if unit_diagonal:
        with catch_warnings():
            simplefilter('ignore', SparseEfficiencyWarning)
            A.setdiag(1)
    else:
        diag = A.diagonal()
        if np.any(diag == 0):
            raise LinAlgError(
                'A is singular: zero entry on diagonal.')
        invdiag = 1/diag
        if trans == "N":
            A = A @ diags_array(invdiag)
        else:
            A = (A.T @ diags_array(invdiag)).T

    # sum duplicates for non-canonical format
    A.sum_duplicates()

    b = np.asanyarray(b)

    if b.ndim not in [1, 2]:
        raise ValueError(
            f'b must have 1 or 2 dims but its shape is {b.shape}.')
    if M != b.shape[0]:
        raise ValueError(
            'The size of the dimensions of A must be equal to '
            'the size of the first dimension of b but the shape of A is '
            f'{A.shape} and the shape of b is {b.shape}.'
        )

    result_dtype = np.promote_types(np.promote_types(A.dtype, np.float32), b.dtype)
    if A.dtype != result_dtype:
        A = A.astype(result_dtype)
    if b.dtype != result_dtype:
        b = b.astype(result_dtype)
    elif not overwrite_b:
        b = b.copy()

    if lower:
        L = A
        U = csc_array((N, N), dtype=result_dtype)
    else:
        L = eye_array(N, dtype=result_dtype, format='csc')
        U = A
        U.setdiag(0)

    L_indices, L_indptr = safely_cast_index_arrays(L, np.intc, "SuperLU")
    U_indices, U_indptr = safely_cast_index_arrays(U, np.intc, "SuperLU")

    x, info = _superlu.gstrs(trans,
                             N, L.nnz, L.data, L_indices, L_indptr,
                             N, U.nnz, U.data, U_indices, U_indptr,
                             b)
    if info:
        raise LinAlgError('A is singular.')

    if not unit_diagonal:
        invdiag = invdiag.reshape(-1, *([1] * (len(x.shape) - 1)))
        x = x * invdiag

    return x

