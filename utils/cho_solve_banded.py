
def cho_solve_banded(cb_and_lower, b, overwrite_b=False, check_finite=True):
    """
    Solve the linear equations ``A x = b``, given the Cholesky factorization of
    the banded Hermitian ``A``.

    The documentation is written assuming array arguments are of specified
    "core" shapes. However, array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    cb_and_lower : tuple, (ndarray, bool)
        The first element of the tuple is the matrix containing the Cholesky factor,
        as provided by `cholesky_banded`. The second element is a boolean flag
        indicating whether the factor is in the lower triangle, as provided *to*
        `cholesky_banded`.
    b : array_like
        Right-hand side
    overwrite_b : bool, optional
        If True, the function will overwrite the values in `b`.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    x : array
        The solution to the system A x = b

    See Also
    --------
    cholesky_banded : Cholesky factorization of a banded matrix

    Notes
    -----

    .. versionadded:: 0.8.0

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import cholesky_banded, cho_solve_banded
    >>> Ab = np.array([[0, 0, 1j, 2, 3j], [0, -1, -2, 3, 4], [9, 8, 7, 6, 9]])
    >>> A = np.diag(Ab[0,2:], k=2) + np.diag(Ab[1,1:], k=1)
    >>> A = A + A.conj().T + np.diag(Ab[2, :])
    >>> c = cholesky_banded(Ab)
    >>> x = cho_solve_banded((c, False), np.ones(5))
    >>> np.allclose(A @ x - np.ones(5), np.zeros(5))
    True

    """
    (cb, lower) = cb_and_lower
    return _cho_solve_banded(cb, b, lower, overwrite_b=overwrite_b,
                             check_finite=check_finite)

