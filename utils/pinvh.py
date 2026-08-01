
def pinvh(a, atol=None, rtol=None, lower=True, return_rank=False,
          check_finite=True):
    """
    Compute the (Moore-Penrose) pseudo-inverse of a Hermitian matrix.

    Calculate a generalized inverse of a complex Hermitian/real symmetric
    matrix using its eigenvalue decomposition and including all eigenvalues
    with 'large' absolute value.

    Parameters
    ----------
    a : (N, N) array_like
        Real symmetric or complex hermetian matrix to be pseudo-inverted

    atol : float, optional
        Absolute threshold term, default value is 0.

        .. versionadded:: 1.7.0

    rtol : float, optional
        Relative threshold term, default value is ``N * eps`` where
        ``eps`` is the machine precision value of the datatype of ``a``.

        .. versionadded:: 1.7.0

    lower : bool, optional
        Whether the pertinent array data is taken from the lower or upper
        triangle of `a`. (Default: lower)
    return_rank : bool, optional
        If True, return the effective rank of the matrix.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    B : (N, N) ndarray
        The pseudo-inverse of matrix `a`.
    rank : int
        The effective rank of the matrix.  Returned if `return_rank` is True.

    Raises
    ------
    LinAlgError
        If eigenvalue algorithm does not converge.

    See Also
    --------
    pinv : Moore-Penrose pseudoinverse of a matrix.

    Examples
    --------

    For a more detailed example see `pinv`.

    >>> import numpy as np
    >>> from scipy.linalg import pinvh
    >>> rng = np.random.default_rng()
    >>> a = rng.standard_normal((9, 6))
    >>> a = np.dot(a, a.T)
    >>> B = pinvh(a)
    >>> np.allclose(a, a @ B @ a)
    True
    >>> np.allclose(B, B @ a @ B)
    True

    """
    a = _asarray_validated(a, check_finite=check_finite)
    s, u = _decomp.eigh(a, lower=lower, check_finite=False, driver='ev')
    t = u.dtype.char.lower()
    maxS = np.max(np.abs(s), initial=0.)

    atol = 0. if atol is None else atol
    rtol = max(a.shape) * np.finfo(t).eps if (rtol is None) else rtol

    if (atol < 0.) or (rtol < 0.):
        raise ValueError("atol and rtol values must be positive.")

    val = atol + maxS * rtol
    above_cutoff = (abs(s) > val)

    psigma_diag = 1.0 / s[above_cutoff]
    u = u[:, above_cutoff]

    B = (u * psigma_diag) @ u.conj().T

    if return_rank:
        return B, len(psigma_diag)
    else:
        return B

