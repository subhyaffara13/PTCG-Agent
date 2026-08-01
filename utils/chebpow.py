
def chebpow(c, pow, maxpower=16):
    """Raise a Chebyshev series to a power.

    Returns the Chebyshev series `c` raised to the power `pow`. The
    argument `c` is a sequence of coefficients ordered from low to high.
    i.e., [1,2,3] is the series  ``T_0 + 2*T_1 + 3*T_2.``

    Parameters
    ----------
    c : array_like
        1-D array of Chebyshev series coefficients ordered from low to
        high.
    pow : integer
        Power to which the series will be raised
    maxpower : integer, optional
        Maximum power allowed. This is mainly to limit growth of the series
        to unmanageable size. Default is 16

    Returns
    -------
    coef : ndarray
        Chebyshev series of power.

    See Also
    --------
    chebadd, chebsub, chebmulx, chebmul, chebdiv

    Examples
    --------
    >>> from numpy.polynomial import chebyshev as C
    >>> C.chebpow([1, 2, 3, 4], 2)
    array([15.5, 22. , 16. , ..., 12.5, 12. ,  8. ])

    """
    # note: this is more efficient than `pu._pow(chebmul, c1, c2)`, as it
    # avoids converting between z and c series repeatedly

    # c is a trimmed copy
    [c] = pu.as_series([c])
    power = int(pow)
    if power != pow or power < 0:
        raise ValueError("Power must be a non-negative integer.")
    elif maxpower is not None and power > maxpower:
        raise ValueError("Power is too large")
    elif power == 0:
        return np.array([1], dtype=c.dtype)
    elif power == 1:
        return c
    else:
        # This can be made more efficient by using powers of two
        # in the usual way.
        zs = _cseries_to_zseries(c)
        prd = zs
        for i in range(2, power + 1):
            prd = np.convolve(prd, zs)
        return _zseries_to_cseries(prd)

