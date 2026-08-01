
def riccati_jn(n, x):
    r"""Compute Riccati-Bessel function of the first kind and its derivative.

    The Riccati-Bessel function of the first kind is defined as :math:`x
    j_n(x)`, where :math:`j_n` is the spherical Bessel function of the first
    kind of order :math:`n`.

    This function computes the value and first derivative of the
    Riccati-Bessel function for all orders up to and including `n`.

    Parameters
    ----------
    n : int
        Maximum order of function to compute
    x : float
        Argument at which to evaluate

    Returns
    -------
    jn : ndarray
        Value of j0(x), ..., jn(x)
    jnp : ndarray
        First derivative j0'(x), ..., jn'(x)

    Notes
    -----
    The computation is carried out via backward recurrence, using the
    relation DLMF 10.51.1 [2]_.

    Wrapper for a Fortran routine created by Shanjie Zhang and Jianming
    Jin [1]_.

    References
    ----------
    .. [1] Zhang, Shanjie and Jin, Jianming. "Computation of Special
           Functions", John Wiley and Sons, 1996.
           https://people.sc.fsu.edu/~jburkardt/f77_src/special_functions/special_functions.html
    .. [2] NIST Digital Library of Mathematical Functions.
           https://dlmf.nist.gov/10.51.E1

    """
    if not (isscalar(n) and isscalar(x)):
        raise ValueError("arguments must be scalars.")
    n = _nonneg_int_or_fail(n, 'n', strict=False)
    if (n == 0):
        n1 = 1
    else:
        n1 = n

    jn = np.empty((n1 + 1,), dtype=np.float64)
    jnp = np.empty_like(jn)

    _rctj(x, out=(jn, jnp))
    return jn[:(n+1)], jnp[:(n+1)]

