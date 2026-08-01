
def savgol_coeffs(window_length, polyorder, deriv=0, delta=1.0, pos=None,
                  use="conv", *, xp=None, device=None):
    """Compute the coefficients for a 1-D Savitzky-Golay FIR filter.

    Parameters
    ----------
    window_length : int
        The length of the filter window (i.e., the number of coefficients).
    polyorder : int
        The order of the polynomial used to fit the samples.
        `polyorder` must be less than `window_length`.
    deriv : int, optional
        The order of the derivative to compute. This must be a
        nonnegative integer. The default is 0, which means to filter
        the data without differentiating.
    delta : float, optional
        The spacing of the samples to which the filter will be applied.
        This is only used if deriv > 0.
    pos : int or None, optional
        If pos is not None, it specifies evaluation position within the
        window. The default is the middle of the window.
    use : str, optional
        Either 'conv' or 'dot'. This argument chooses the order of the
        coefficients. The default is 'conv', which means that the
        coefficients are ordered to be used in a convolution. With
        use='dot', the order is reversed, so the filter is applied by
        dotting the coefficients with the data set.
    xp : array_namespace, optional
        Optional array namespace.
        Should be compatible with the array API standard, or supported by
        array-api-compat.
        Default: ``numpy``
    device : any
        optional device specification for output. Should match one of the
        supported device specifications in ``xp``.

    Returns
    -------
    coeffs : 1-D ndarray
        The filter coefficients.

    See Also
    --------
    savgol_filter

    Notes
    -----
    .. versionadded:: 0.14.0

    References
    ----------
    A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of Data by
    Simplified Least Squares Procedures. Analytical Chemistry, 1964, 36 (8),
    pp 1627-1639.
    Jianwen Luo, Kui Ying, and Jing Bai. 2005. Savitzky-Golay smoothing and
    differentiation filter for even number data. Signal Process.
    85, 7 (July 2005), 1429-1434.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.signal import savgol_coeffs
    >>> savgol_coeffs(5, 2)
    array([-0.08571429,  0.34285714,  0.48571429,  0.34285714, -0.08571429])
    >>> savgol_coeffs(5, 2, deriv=1)
    array([ 2.00000000e-01,  1.00000000e-01,  2.07548111e-16, -1.00000000e-01,
           -2.00000000e-01])

    Note that use='dot' simply reverses the coefficients.

    >>> savgol_coeffs(5, 2, pos=3)
    array([ 0.25714286,  0.37142857,  0.34285714,  0.17142857, -0.14285714])
    >>> savgol_coeffs(5, 2, pos=3, use='dot')
    array([-0.14285714,  0.17142857,  0.34285714,  0.37142857,  0.25714286])
    >>> savgol_coeffs(4, 2, pos=3, deriv=1, use='dot')
    array([0.45,  -0.85,  -0.65,  1.05])

    `x` contains data from the parabola x = t**2, sampled at
    t = -1, 0, 1, 2, 3.  `c` holds the coefficients that will compute the
    derivative at the last position.  When dotted with `x` the result should
    be 6.

    >>> x = np.array([1, 0, 1, 4, 9])
    >>> c = savgol_coeffs(5, 2, pos=4, deriv=1, use='dot')
    >>> c.dot(x)
    6.0
    """

    # An alternative method for finding the coefficients when deriv=0 is
    #    t = np.arange(window_length)
    #    unit = (t == pos).astype(int)
    #    coeffs = np.polyval(np.polyfit(t, unit, polyorder), t)
    # The method implemented here is faster.

    # To recreate the table of sample coefficients shown in the chapter on
    # the Savitzy-Golay filter in the Numerical Recipes book, use
    #    window_length = nL + nR + 1
    #    pos = nL + 1
    #    c = savgol_coeffs(window_length, M, pos=pos, use='dot')

    if polyorder >= window_length:
        raise ValueError("polyorder must be less than window_length.")

    halflen, rem = divmod(window_length, 2)

    if pos is None:
        if rem == 0:
            pos = halflen - 0.5
        else:
            pos = halflen

    if not (0 <= pos < window_length):
        raise ValueError("pos must be nonnegative and less than "
                         "window_length.")

    if use not in ['conv', 'dot']:
        raise ValueError("`use` must be 'conv' or 'dot'")

    # cf windows/_windows.py
    xp = np_compat if xp is None else array_namespace(xp.empty(0))

    if deriv > polyorder:
        coeffs = xp.zeros(window_length, dtype=xp.float64, device=device)
        return coeffs

    # Form the design matrix A. The columns of A are powers of the integers
    # from -pos to window_length - pos - 1. The powers (i.e., rows) range
    # from 0 to polyorder. (That is, A is a vandermonde matrix, but not
    # necessarily square.)
    x = xp.arange(-pos, window_length - pos, dtype=xp.float64, device=device)

    if use == "conv":
        # Reverse so that result can be used in a convolution.
        x = xp.flip(x)

    order = xp.reshape(
        xp.arange(polyorder + 1, dtype=xp.float64, device=device), (-1, 1)
    )
    A = x ** order

    # y determines which order derivative is returned.
    y = xp.zeros(polyorder + 1, dtype=xp.float64, device=device)
    # The coefficient assigned to y[deriv] scales the result to take into
    # account the order of the derivative and the sample spacing.
    y = xpx.at(y, deriv).set(float_factorial(deriv) / (delta ** deriv))

    # Find the least-squares solution of A*c = y
    coeffs, _, _, _ = _pu._lstsq(A, y, xp=xp)

    return coeffs

