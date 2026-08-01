
def return_NdBSpline(fp, tck, degrees):
    """
    Build a 2D ``NdBSpline`` from knot vectors and a coefficient grid.

    Parameters
    ----------
    fp : float
        Residual sum of squares of the produced fit (kept for upstream use).
    tck : tuple
        Tuple ``(tx, ty, C)`` where ``tx``, ``ty`` are knot vectors and ``C``
        is a coefficient array with shape ``(nx - kx - 1, ny - ky - 1)`` or
        a compatible shape that can be reshaped to that.
    degrees : tuple of int
        Degrees ``(kx, ky)`` along x and y.

    Returns
    -------
    NdBSpline
        The constructed 2D spline.

    Notes
    -----
    Only repacks the coefficient grid; ``fp`` is not used internally here.
    """
    nx, ny = len(tck[0]), len(tck[1])
    kx, ky = degrees
    c = tck[2].reshape(nx - kx - 1, ny - ky - 1)
    return NdBSpline((tck[0], tck[1]), c, degrees)

