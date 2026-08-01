
def is_sptriangular(A):
    """Returns 2-tuple indicating lower/upper triangular structure for sparse ``A``.

    Checks for triangular structure in ``A``. The result is summarized in
    two boolean values ``lower`` and ``upper`` to designate whether ``A`` is
    lower triangular or upper triangular respectively. Diagonal ``A`` will
    result in both being True. Non-triangular structure results in False for both.

    Only the sparse structure is used here. Values are not checked for zeros.

    This function will convert a copy of ``A`` to CSC format if it is not already
    CSR or CSC format. So it may be more efficient to convert it yourself if you
    have other uses for the CSR/CSC version.

    If ``A`` is not square, the portions outside the upper left square of the
    matrix do not affect its triangular structure. You probably want to work
    with the square portion of the matrix, though it is not requred here.

    Parameters
    ----------
    A : SciPy sparse array or matrix
        A sparse matrix preferrably in CSR or CSC format.

    Returns
    -------
    lower, upper : 2-tuple of bool
        Whether `A` is lower / upper triangular.

        .. versionadded:: 1.15.0

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csc_array, eye_array
    >>> from scipy.sparse.linalg import is_sptriangular
    >>> A = csc_array([[3, 0, 0], [1, -1, 0], [2, 0, 1]], dtype=float)
    >>> is_sptriangular(A)
    (True, False)
    >>> D = eye_array(3, format='csr')
    >>> is_sptriangular(D)
    (True, True)
    """
    if not (issparse(A) and A.format in ("csc", "csr", "coo", "dia", "dok", "lil")):
        warn('is_sptriangular needs sparse and not BSR format. Converting to CSR.',
             SparseEfficiencyWarning, stacklevel=2)
        A = csr_array(A)

    # bsr is better off converting to csr
    if A.format == "dia":
        return A.offsets.max() <= 0, A.offsets.min() >= 0
    elif A.format == "coo":
        rows, cols = A.coords
        return (cols <= rows).all(), (cols >= rows).all()
    elif A.format == "dok":
        return all(c <= r for r, c in A.keys()), all(c >= r for r, c in A.keys())
    elif A.format == "lil":
        lower = all(col <= row for row, cols in enumerate(A.rows) for col in cols)
        upper = all(col >= row for row, cols in enumerate(A.rows) for col in cols)
        return lower, upper
    # format in ("csc", "csr")
    indptr, indices = A.indptr, A.indices
    N = len(indptr) - 1

    lower, upper = True, True
    # check middle, 1st, last col (treat as CSC and switch at end if CSR)
    for col in [N // 2, 0, -1]:
        rows = indices[indptr[col]:indptr[col + 1]]
        upper = upper and (col >= rows).all()
        lower = lower and (col <= rows).all()
        if not upper and not lower:
            return False, False
    # check all cols
    cols = np.repeat(np.arange(N), np.diff(indptr))
    rows = indices
    upper = upper and (cols >= rows).all()
    lower = lower and (cols <= rows).all()
    if A.format == 'csr':
        return upper, lower
    return lower, upper

