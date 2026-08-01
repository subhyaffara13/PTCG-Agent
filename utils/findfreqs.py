
def findfreqs(num, den, N, kind='ba'):
    """
    Find array of frequencies for computing the response of an analog filter.

    Parameters
    ----------
    num, den : array_like, 1-D
        The polynomial coefficients of the numerator and denominator of the
        transfer function of the filter or LTI system, where the coefficients
        are ordered from highest to lowest degree. Or, the roots  of the
        transfer function numerator and denominator (i.e., zeroes and poles).
    N : int
        The length of the array to be computed.
    kind : str {'ba', 'zp'}, optional
        Specifies whether the numerator and denominator are specified by their
        polynomial coefficients ('ba'), or their roots ('zp').

    Returns
    -------
    w : (N,) ndarray
        A 1-D array of frequencies, logarithmically spaced.

    Examples
    --------
    Find a set of nine frequencies that span the "interesting part" of the
    frequency response for the filter with the transfer function

        H(s) = s / (s^2 + 8s + 25)

    >>> from scipy import signal
    >>> signal.findfreqs([1, 0], [1, 8, 25], N=9)
    array([  1.00000000e-02,   3.16227766e-02,   1.00000000e-01,
             3.16227766e-01,   1.00000000e+00,   3.16227766e+00,
             1.00000000e+01,   3.16227766e+01,   1.00000000e+02])
    """
    xp = array_namespace(num, den)
    num, den = map(xp.asarray, (num, den))

    if kind == 'ba':
        ep = xpx.atleast_nd(_pu.polyroots(den, xp=xp), ndim=1, xp=xp)
        tz = xpx.atleast_nd(_pu.polyroots(num, xp=xp), ndim=1, xp=xp)
    elif kind == 'zp':
        ep = xpx.atleast_nd(den, ndim=1, xp=xp)
        tz = xpx.atleast_nd(num, ndim=1, xp=xp)
    else:
        raise ValueError("input must be one of {'ba', 'zp'}")

    ep = xp_float_to_complex(ep, xp=xp)
    tz = xp_float_to_complex(tz, xp=xp)

    if ep.shape[0] == 0:
        ep = xp.asarray([-1000], dtype=ep.dtype)

    ez = xp.concat((
        ep[xp.imag(ep) >= 0],
        tz[(xp.abs(tz) < 1e5) & (xp.imag(tz) >= 0)]
    ))

    integ = xp.astype(xp.abs(ez) < 1e-10, ez.dtype) # XXX True->1, False->0
    hfreq = xp.round(
        xp.log10(xp.max(3*xp.abs(xp.real(ez) + integ) + 1.5*xp.imag(ez))) + 0.5
    )

    # the fudge factor is for backwards compatibility: round(-1.5) can be -1 or -2
    # depending on the floating-point jitter in -1.5
    fudge = 1e-14 if is_jax(xp) else 0
    lfreq = xp.round(
        xp.log10(0.1*xp.min(xp.abs(xp.real(ez + integ)) + 2*xp.imag(ez))) - 0.5 - fudge
    )

    w = _logspace(lfreq, hfreq, N, xp=xp)
    return w

