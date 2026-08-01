
def riccati_yn(n, x):
    """Compute Riccati-Bessel function of the second kind and its derivative.

    The Riccati-Bessel function of the second kind is defined here as :math:`+x
    y_n(x)`, where :math:`y_n` is the spherical Bessel function of the second
    kind of order :math:`n`. *Note that this is in contrast to a common convention
    that includes a minus sign in the definition.*

    This function computes the value and first derivative of the function for
    all orders up to and including `n`.

    Parameters
    ----------
    n : int
        Maximum order of function to compute
    x : float
        Argument at which to evaluate

    Returns
    -------
    yn : ndarray
        Value of y0(x), ..., yn(x)
    ynp : ndarray
        First derivative y0'(x), ..., yn'(x)

    Notes
    -----
    The computation is carried out via ascending recurrence, using the
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

    yn = np.empty((n1 + 1,), dtype=np.float64)
    ynp = np.empty_like(yn)
    _rcty(x, out=(yn, ynp))

    return yn[:(n+1)], ynp[:(n+1)]

