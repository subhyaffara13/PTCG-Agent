
def polyvander(x, deg):
    """Vandermonde matrix of given degree.

    Returns the Vandermonde matrix of degree `deg` and sample points
    `x`. The Vandermonde matrix is defined by

    .. math:: V[..., i] = x^i,

    where ``0 <= i <= deg``. The leading indices of `V` index the elements of
    `x` and the last index is the power of `x`.

    If `c` is a 1-D array of coefficients of length ``n + 1`` and `V` is the
    matrix ``V = polyvander(x, n)``, then ``np.dot(V, c)`` and
    ``polyval(x, c)`` are the same up to roundoff. This equivalence is
    useful both for least squares fitting and for the evaluation of a large
    number of polynomials of the same degree and sample points.

    Parameters
    ----------
    x : array_like
        Array of points. The dtype is converted to float64 or complex128
        depending on whether any of the elements are complex. If `x` is
        scalar it is converted to a 1-D array.
    deg : int
        Degree of the resulting matrix.

    Returns
    -------
    vander : ndarray.
        The Vandermonde matrix. The shape of the returned matrix is
        ``x.shape + (deg + 1,)``, where the last index is the power of `x`.
        The dtype will be the same as the converted `x`.

    See Also
    --------
    polyvander2d, polyvander3d

    Examples
    --------
    The Vandermonde matrix of degree ``deg = 5`` and sample points
    ``x = [-1, 2, 3]`` contains the element-wise powers of `x`
    from 0 to 5 as its columns.

    >>> from numpy.polynomial import polynomial as P
    >>> x, deg = [-1, 2, 3], 5
    >>> P.polyvander(x=x, deg=deg)
    array([[  1.,  -1.,   1.,  -1.,   1.,  -1.],
           [  1.,   2.,   4.,   8.,  16.,  32.],
           [  1.,   3.,   9.,  27.,  81., 243.]])

    """
    ideg = pu._as_int(deg, "deg")
    if ideg < 0:
        raise ValueError("deg must be non-negative")

    x = np.array(x, copy=None, ndmin=1) + 0.0
    dims = (ideg + 1,) + x.shape
    dtyp = x.dtype
    v = np.empty(dims, dtype=dtyp)
    v[0] = x * 0 + 1
    if ideg > 0:
        v[1] = x
        for i in range(2, ideg + 1):
            v[i] = v[i - 1] * x
    return np.moveaxis(v, 0, -1)

