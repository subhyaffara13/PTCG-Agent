
def cspline2d(signal, lamb=0.0, precision=-1.0):
    """
    Coefficients for 2-D cubic (3rd order) B-spline.

    Return the third-order B-spline coefficients over a regularly spaced
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
    xp = array_namespace(signal)
    signal = np.asarray(signal)

    if precision < 0.0 or precision >= 1.0:
        if signal.dtype in [np.float32, np.complex64]:
            precision = 1e-3
        else:
            precision = 1e-6

    if lamb <= 1 / 144.0:
        # Normal cubic spline
        r = -2 + math.sqrt(3.0)
        out = symiirorder_nd(
            symiirorder1, signal, -r * 6.0, r, precision=precision, axis=-1)
        out = symiirorder_nd(
            symiirorder1, out, -r * 6.0, r, precision=precision, axis=0)
        return out

    r, omega = compute_root_from_lambda(lamb)
    out = symiirorder_nd(symiirorder2, signal, r, omega,
                         precision=precision, axis=-1)
    out = symiirorder_nd(symiirorder2, out, r, omega,
                         precision=precision, axis=0)
    return xp.asarray(out)

