
def polyvalnd(pts, c):
    r"""
    Evaluate an N-D polynomial at points.

    This function returns the values:

    .. math::
        p(pts, c) = \sum_{i_1, i_2, \dots, i_n}
        c_{i_1, i_2, \dots, i_n} * x_1^{i_1} * x_2^{i_2} \dots x_n^{i_n}

    where :math:`x_1, x_2, \dots, x_n = pts`.
    Note that `pts` may also be an `(n, m)` array.

    The parameters in `pts` are converted to arrays only if they are
    tuples or lists, otherwise they are treated as scalars and
    they must have the same shape after conversion. In either case, either
    the elements of `pts` or their elements must support multiplication and
    addition both with themselves and with the elements of `c`.

    If `c` has fewer than N dimensions, ones are implicitly appended to its
    shape to make it N-D. The shape of the result will be c.shape[N:] +
    pts[0].shape.

    Parameters
    ----------
    pts : tuple or list of array_like, compatible objects
        The N-dimensional series is evaluated at the points
        ``(x_1, x_2, ..., x_n)`` provided in the `pts` iterable, where
        all elements must have the same shape. If any element is a list
        or tuple, it is first converted to an ndarray, otherwise it is
        left unchanged and if it isn't an ndarray it is treated as a scalar.
    c : array_like
        Array of coefficients ordered so that the coefficient of the term of
        multi-degree i,j,k,... is contained in ``c[i,j,k,...]``. If `c` has
        dimension greater than N, the remaining indices enumerate multiple
        sets of coefficients.

    Returns
    -------
    values : ndarray, compatible object
        The values of the multidimensional polynomial on points formed with
        N-tuples of corresponding values from `pts`.

    See Also
    --------
    polyval, polyval2d, polyval3d

    """
    return pu._valnd(polyval, c, *pts)

