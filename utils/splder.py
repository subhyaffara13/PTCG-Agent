
def splder(tck, n=1, xp=None):
    # see the docstring of `_fitpack_py/splder`
    if n < 0:
        return splantider(tck, -n)

    t, c, k = tck

    if xp is None:
        xp = array_namespace(t, c)

    if n > k:
        raise ValueError(f"Order of derivative (n = {n!r}) must be <= "
                         f"order of spline (k = {tck[2]!r})")

    # Extra axes for the trailing dims of the `c` array:
    sh = (slice(None),) + ((None,)*len(c.shape[1:]))

    with np.errstate(invalid='raise', divide='raise'):
        try:
            for j in range(n):
                # See e.g. Schumaker, Spline Functions: Basic Theory, Chapter 5

                # Compute the denominator in the differentiation formula.
                # (and append trailing dims, if necessary)
                dt = t[k+1:-1] - t[1:-k-1]
                dt = dt[sh]
                # Compute the new coefficients
                c = (c[1:-1-k, ...] - c[:-2-k, ...]) * k / dt
                # Pad coefficient array to same size as knots (FITPACK
                # convention)
                c = concat_1d(xp, c, xp.zeros((k,) + c.shape[1:]))
                # Adjust knots
                t = t[1:-1]
                k -= 1
        except FloatingPointError as e:
            raise ValueError("The spline has internal repeated knots "
                              f"and is not differentiable {n} times") from e

    return t, c, k


def splder(tck, n=1):
    """
    Compute the spline representation of the derivative of a given spline.

    .. legacy:: function

        Specifically, we recommend constructing a `BSpline` object and using its
        ``derivative`` method.

    Parameters
    ----------
    tck : BSpline instance or tuple
        BSpline instance or a tuple (t,c,k) containing the vector of knots,
        the B-spline coefficients, and the degree of the spline whose 
        derivative to compute
    n : int, optional
        Order of derivative to evaluate. Default: 1

    Returns
    -------
    `BSpline` instance or tuple
        Spline of order k2=k-n representing the derivative
        of the input spline.
        A tuple is returned if the input argument `tck` is a tuple, otherwise
        a BSpline object is constructed and returned.

    See Also
    --------
    splantider, splev, spalde
    BSpline

    Notes
    -----

    .. versionadded:: 0.13.0

    Examples
    --------
    This can be used for finding maxima of a curve:

    >>> from scipy.interpolate import splrep, splder, sproot
    >>> import numpy as np
    >>> x = np.linspace(0, 10, 70)
    >>> y = np.sin(x)
    >>> spl = splrep(x, y, k=4)

    Now, differentiate the spline and find the zeros of the
    derivative. (NB: `sproot` only works for order 3 splines, so we
    fit an order 4 spline):

    >>> dspl = splder(spl)
    >>> sproot(dspl) / np.pi
    array([ 0.50000001,  1.5       ,  2.49999998])

    This agrees well with roots :math:`\\pi/2 + n\\pi` of
    :math:`\\cos(x) = \\sin'(x)`.

    A comparison between `splev`, `splder` and `spalde` to compute the derivatives of a 
    B-spline can be found in the `spalde` examples section.

    """
    if isinstance(tck, BSpline):
        return tck.derivative(n)
    else:
        return _impl.splder(tck, n)

