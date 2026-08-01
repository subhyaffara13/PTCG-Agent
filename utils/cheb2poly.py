
def cheb2poly(c):
    """
    Convert a Chebyshev series to a polynomial.

    Convert an array representing the coefficients of a Chebyshev series,
    ordered from lowest degree to highest, to an array of the coefficients
    of the equivalent polynomial (relative to the "standard" basis) ordered
    from lowest to highest degree.

    Parameters
    ----------
    c : array_like
        1-D array containing the Chebyshev series coefficients, ordered
        from lowest order term to highest.

    Returns
    -------
    pol : ndarray
        1-D array containing the coefficients of the equivalent polynomial
        (relative to the "standard" basis) ordered from lowest order term
        to highest.

    See Also
    --------
    poly2cheb

    Notes
    -----
    The easy way to do conversions between polynomial basis sets
    is to use the convert method of a class instance.

    Examples
    --------
    >>> from numpy import polynomial as P
    >>> c = P.Chebyshev(range(4))
    >>> c
    Chebyshev([0., 1., 2., 3.], domain=[-1.,  1.], window=[-1.,  1.], symbol='x')
    >>> p = c.convert(kind=P.Polynomial)
    >>> p
    Polynomial([-2., -8.,  4., 12.], domain=[-1.,  1.], window=[-1.,  1.], ...
    >>> P.chebyshev.cheb2poly(range(4))
    array([-2.,  -8.,   4.,  12.])

    """
    from .polynomial import polyadd, polymulx, polysub

    [c] = pu.as_series([c])
    n = len(c)
    if n < 3:
        return c
    else:
        c0 = c[-2]
        c1 = c[-1]
        # i is the current degree of c1
        for i in range(n - 1, 1, -1):
            tmp = c0
            c0 = polysub(c[i - 2], c1)
            c1 = polyadd(tmp, polymulx(c1) * 2)
        return polyadd(c0, polymulx(c1))

