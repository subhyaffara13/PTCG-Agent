
def zpk2tf(z, p, k):
    r"""
    Return polynomial transfer function representation from zeros and poles.

    Parameters
    ----------
    z : array_like
        Zeros of the transfer function.
    p : array_like
        Poles of the transfer function.
    k : float
        System gain.

    Returns
    -------
    b : ndarray
        Numerator polynomial coefficients.
    a : ndarray
        Denominator polynomial coefficients.

    Examples
    --------
    Find the polynomial representation of a transfer function H(s)
    using its 'zpk' (Zero-Pole-Gain) representation.

    .. math::

        H(z) = 5 \frac
        { (s - 2)(s - 6) }
        { (s - 1)(s - 8) }

    >>> from scipy.signal import zpk2tf
    >>> z   = [2,   6]
    >>> p   = [1,   8]
    >>> k   = 5
    >>> zpk2tf(z, p, k)
    (   array([  5., -40.,  60.]), array([ 1., -9.,  8.]))
    """
    xp = array_namespace(z, p)
    z, p = map(xp.asarray, (z, p))
    k = xp.asarray(k, dtype=xp.result_type(xp.real(z), xp.real(p), k))
    if xp.isdtype(k.dtype, "integral"):
        k = xp.astype(k, xp.float64)

    z = xpx.atleast_nd(z, ndim=1, xp=xp)
    k = xpx.atleast_nd(k, ndim=1, xp=xp)

    if z.ndim > 1:
        temp = _pu.poly(z[0, ...], xp=xp)
        result_dtype = xp_result_type(temp, k, force_floating=True, xp=xp)
        b = xp.empty((z.shape[0], z.shape[1] + 1), dtype=result_dtype)
        if k.shape[0] == 1:
            k = [k[0]] * z.shape[0]
        for i in range(z.shape[0]):
            k_i = xp.asarray(k[i], dtype=result_dtype)
            poly_i = xp.asarray(_pu.poly(z[i, ...], xp=xp), dtype=result_dtype)
            b_i = k_i * poly_i
            b = xpx.at(b)[i, ...].set(b_i)
    else:
        # Use xp.multiply to work around torch type promotion
        # non-compliance for operations between 0d and higher
        # dimensional arrays.
        b = xp.multiply(k, _pu.poly(z, xp=xp))

    a = _pu.poly(p, xp=xp)
    a = xpx.atleast_nd(xp.asarray(a), ndim=1, xp=xp)

    return b, a

