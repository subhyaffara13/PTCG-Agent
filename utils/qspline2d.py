import math


def qspline2d(signal, lamb=0.0, precision=-1.0):
    """
    Coefficients for 2-D quadratic (2nd order) B-spline.

    Return the second-order B-spline coefficients over a regularly spaced
    input grid for the two-dimensional input image.

    Parameters
    ----------
    signal : ndarray
        The input signal.
    lamb : float
        Specifies the amount of smoothing in the transfer function.
    precision : float
        Specifies the precision for computing the infinite sum needed to apply
        mirror-symmetric boundary conditions.

    Returns
    -------
    output : ndarray
        The filtered signal.
    """
    if precision < 0.0 or precision >= 1.0:
        if signal.dtype in [float32, complex64]:
            precision = 1e-3
        else:
            precision = 1e-6

    if lamb > 0:
        raise ValueError('lambda must be negative or zero')

    # normal quadratic spline
    r = -3 + 2 * math.sqrt(2.0)
    c0 = -r * 8.0
    z1 = r

    out = symiirorder_nd(symiirorder1, signal, c0, z1, precision, axis=-1)
    out = symiirorder_nd(symiirorder1, out, c0, z1, precision, axis=0)
    return out

