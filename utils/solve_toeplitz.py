
def solve_toeplitz(c_or_cr, b, check_finite=True):
    r"""Solve the equation ``T @ x = b`` for ``x``, where ``T`` is a Toeplitz
    matrix defined by `c_or_cr`.

    The Toeplitz matrix has constant diagonals, with ``c`` as its first column
    and ``r`` as its first row. If ``r`` is not given, ``r == conjugate(c)`` is
    assumed.

    The documentation is written assuming array arguments are of specified
    "core" shapes. However, array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    c_or_cr : array_like or tuple of (array_like, array_like)
        The vector ``c``, or a tuple of arrays (``c``, ``r``). If not
        supplied, ``r = conjugate(c)`` is assumed; in this case, if c[0] is
        real, the Toeplitz matrix is Hermitian. r[0] is ignored; the first row
        of the Toeplitz matrix is ``[c[0], r[1:]]``.
    b : (M,) or (M, K) array_like
        Right-hand side in ``T x = b``.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (result entirely NaNs) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : (M,) or (M, K) ndarray
        The solution to the system ``T @ x = b``. Shape of return matches shape
        of `b`.

    See Also
    --------
    toeplitz : Toeplitz matrix

    Notes
    -----
    The solution is computed using Levinson-Durbin recursion, which is faster
    than generic least-squares methods, but can be less numerically stable.

    Examples
    --------
    Solve the Toeplitz system ``T @ x = b``, where::

            [ 1 -1 -2 -3]       [1]
        T = [ 3  1 -1 -2]   b = [2]
            [ 6  3  1 -1]       [2]
            [10  6  3  1]       [5]

    To specify the Toeplitz matrix, only the first column and the first
    row are needed.

    >>> import numpy as np
    >>> c = np.array([1, 3, 6, 10])    # First column of T
    >>> r = np.array([1, -1, -2, -3])  # First row of T
    >>> b = np.array([1, 2, 2, 5])

    >>> from scipy.linalg import solve_toeplitz, toeplitz
    >>> x = solve_toeplitz((c, r), b)
    >>> x
    array([ 1.66666667, -1.        , -2.66666667,  2.33333333])

    Check the result by creating the full Toeplitz matrix and
    multiplying it by ``x``.  We should get `b`.

    >>> T = toeplitz(c, r)
    >>> T.dot(x)
    array([ 1.,  2.,  2.,  5.])

    """
    # If numerical stability of this algorithm is a problem, a future
    # developer might consider implementing other O(N^2) Toeplitz solvers,
    # such as GKO (https://www.jstor.org/stable/2153371) or Bareiss.
    c, r = c_or_cr if isinstance(c_or_cr, tuple) else (c_or_cr, np.conjugate(c_or_cr))
    return _solve_toeplitz(c, r, b, check_finite)

