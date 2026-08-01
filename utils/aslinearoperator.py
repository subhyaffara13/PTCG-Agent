
def aslinearoperator(A):
    """Return `A` as a `LinearOperator`.

    See the `LinearOperator` documentation for additional information.

    Parameters
    ----------
    A : object
        Object to convert to a `LinearOperator`. May be any one of the following types:

        - `numpy.ndarray`
        - `numpy.matrix`
        - `scipy.sparse` array
          (e.g. `~scipy.sparse.csr_array`, `~scipy.sparse.lil_array`, etc.)
        - `LinearOperator`
        - An object with ``.shape`` and ``.matvec`` attributes

    Returns
    -------
    B : LinearOperator
        A `LinearOperator` corresponding with `A`

    Notes
    -----
    If `A` has no ``.dtype`` attribute, the data type is determined by calling
    :func:`LinearOperator.matvec()` - set the ``.dtype`` attribute to prevent this
    call upon the linear operator creation.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse.linalg import aslinearoperator
    >>> M = np.array([[1,2,3],[4,5,6]], dtype=np.int32)
    >>> aslinearoperator(M)
    <2x3 MatrixLinearOperator with dtype=int32>
    """
    if isinstance(A, LinearOperator):
        return A

    # https://github.com/data-apis/array-api-compat/issues/388
    if is_array_api_obj(A) and not isinstance(A, np.matrix):
        xp = array_namespace(A)
        if is_pydata_sparse_array(A) and not SCIPY_ARRAY_API:
            pass  # skip `atleast_nd`, since `xp=np` does not work with `sparse`
        else:
            A = xpx.atleast_nd(A, ndim=2, xp=xp)
        return MatrixLinearOperator(A, xp=xp)

    if issparse(A):
        return MatrixLinearOperator(A)

    if isinstance(A, np.matrix):
        A = np.atleast_2d(np.asarray(A))
        return MatrixLinearOperator(A)

    if hasattr(A, "shape") and hasattr(A, "matvec"):
        rmatvec = None
        rmatmat = None
        dtype = None

        if hasattr(A, "rmatvec"):
            rmatvec = A.rmatvec
        if hasattr(A, "rmatmat"):
            rmatmat = A.rmatmat
        if hasattr(A, "dtype"):
            dtype = A.dtype
        return LinearOperator(
            A.shape, A.matvec, rmatvec=rmatvec, rmatmat=rmatmat, dtype=dtype
        )

    raise TypeError("type not understood")

