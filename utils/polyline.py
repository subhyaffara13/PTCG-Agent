
def polyline(off, scl):
    """
    Returns an array representing a linear polynomial.

    Parameters
    ----------
    off, scl : scalars
        The "y-intercept" and "slope" of the line, respectively.

    Returns
    -------
    y : ndarray
        This module's representation of the linear polynomial ``off +
        scl*x``.

    See Also
    --------
    numpy.polynomial.chebyshev.chebline
    numpy.polynomial.legendre.legline
    numpy.polynomial.laguerre.lagline
    numpy.polynomial.hermite.hermline
    numpy.polynomial.hermite_e.hermeline

    Examples
    --------
    >>> from numpy.polynomial import polynomial as P
    >>> P.polyline(1, -1)
    array([ 1, -1])
    >>> P.polyval(1, P.polyline(1, -1))  # should be 0
    0.0

    """
    if scl != 0:
        return np.array([off, scl])
    else:
        return np.array([off])

