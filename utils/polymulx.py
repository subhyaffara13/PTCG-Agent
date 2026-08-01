
def polymulx(c):
    """Multiply a polynomial by x.

    Multiply the polynomial `c` by x, where x is the independent
    variable.


    Parameters
    ----------
    c : array_like
        1-D array of polynomial coefficients ordered from low to
        high.

    Returns
    -------
    out : ndarray
        Array representing the result of the multiplication.

    See Also
    --------
    polyadd, polysub, polymul, polydiv, polypow

    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> c = (1, 2, 3)
    >>> P.polymulx(c)
    array([0., 1., 2., 3.])

    """
    # c is a trimmed copy
    [c] = pu.as_series([c])
    # The zero series needs special treatment
    if len(c) == 1 and c[0] == 0:
        return c

    prd = np.empty(len(c) + 1, dtype=c.dtype)
    prd[0] = c[0] * 0
    prd[1:] = c
    return prd

