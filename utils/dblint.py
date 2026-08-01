
def dblint(xa, xb, ya, yb, tck):
    """Evaluate the integral of a spline over area [xa,xb] x [ya,yb].

    Parameters
    ----------
    xa, xb : float
        The end-points of the x integration interval.
    ya, yb : float
        The end-points of the y integration interval.
    tck : list [tx, ty, c, kx, ky]
        A sequence of length 5 returned by bisplrep containing the knot
        locations tx, ty, the coefficients c, and the degrees kx, ky
        of the spline.

    Returns
    -------
    integ : float
        The value of the resulting integral.
    """
    tx, ty, c, kx, ky = tck
    return _fitpack.dblint(tx, ty, c, kx, ky, xa, xb, ya, yb)

