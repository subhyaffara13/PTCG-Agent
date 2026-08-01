
def spbandwidth(A):
    """Return the lower and upper bandwidth of a 2D numeric array.

    Computes the lower and upper limits on the bandwidth of the
    sparse 2D array ``A``. The result is summarized as a 2-tuple
    of positive integers ``(lo, hi)``. A zero denotes no sub/super
    diagonal entries on that side (triangular). The maximum value
    for ``lo`` (``hi``) is one less than the number of rows(cols).

    Only the sparse structure is used here. Values are not checked for zeros.

    Parameters
    ----------
    A : SciPy sparse array or matrix
        A sparse matrix preferrably in CSR or CSC format.

    Returns
    -------
    below, above : 2-tuple of int
        The distance to the farthest non-zero diagonal below/above the
        main diagonal.

        .. versionadded:: 1.15.0

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse.linalg import spbandwidth
    >>> from scipy.sparse import csc_array, eye_array
    >>> A = csc_array([[3, 0, 0], [1, -1, 0], [2, 0, 1]], dtype=float)
    >>> spbandwidth(A)
    (2, 0)
    >>> D = eye_array(3, format='csr')
    >>> spbandwidth(D)
    (0, 0)
    """
    if not (issparse(A) and A.format in ("csc", "csr", "coo", "dia", "dok")):
        warn('spbandwidth needs sparse format not LIL and BSR. Converting to CSR.',
             SparseEfficiencyWarning, stacklevel=2)
        A = csr_array(A)

    # bsr and lil are better off converting to csr
    if A.format == "dia":
        return max(0, -A.offsets.min().item()), max(0, A.offsets.max().item())
    if A.format in ("csc", "csr"):
        indptr, indices = A.indptr, A.indices
        N = len(indptr) - 1
        gap = np.repeat(np.arange(N), np.diff(indptr)) - indices
        if A.format == 'csr':
            gap = -gap
    elif A.format == "coo":
        gap = A.coords[1] - A.coords[0]
    elif A.format == "dok":
        gap = [(c - r) for r, c in A.keys()] + [0]
        return -min(gap), max(gap)
    return max(-np.min(gap).item(), 0), max(np.max(gap).item(), 0)

