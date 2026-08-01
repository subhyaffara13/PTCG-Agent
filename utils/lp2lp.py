
def lp2lp(b, a, wo=1.0):
    r"""
    Transform a lowpass filter prototype to a different frequency.

    Return an analog low-pass filter with cutoff frequency `wo`
    from an analog low-pass filter prototype with unity cutoff frequency, in
    transfer function ('ba') representation.

    Parameters
    ----------
    b : array_like, shape (M,)
        Numerator polynomial coefficients. Must be 1-D.
    a : array_like, shape (N,)
        Denominator polynomial coefficients. Must be 1-D.
    wo : float
        Desired cutoff, as angular frequency (e.g. rad/s).
        Defaults to no change.

    Returns
    -------
    b : array_like
        Numerator polynomial coefficients of the transformed low-pass filter.
    a : array_like
        Denominator polynomial coefficients of the transformed low-pass filter.

    See Also
    --------
    lp2hp, lp2bp, lp2bs, bilinear
    lp2lp_zpk

    Notes
    -----
    This is derived from the s-plane substitution

    .. math:: s \rightarrow \frac{s}{\omega_0}

    Examples
    --------

    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt

    >>> lp = signal.lti([1.0], [1.0, 1.0])
    >>> lp2 = signal.lti(*signal.lp2lp(lp.num, lp.den, 2))
    >>> w, mag_lp, p_lp = lp.bode()
    >>> w, mag_lp2, p_lp2 = lp2.bode(w)

    >>> plt.plot(w, mag_lp, label='Lowpass')
    >>> plt.plot(w, mag_lp2, label='Transformed Lowpass')
    >>> plt.semilogx()
    >>> plt.grid(True)
    >>> plt.xlabel('Frequency [rad/s]')
    >>> plt.ylabel('Amplitude [dB]')
    >>> plt.legend()

    """
    xp = array_namespace(a, b)
    a, b = map(xp.asarray, (a, b))
    a, b = xp_promote(a, b, force_floating=True, xp=xp)
    a = xpx.atleast_nd(a, ndim=1, xp=xp)
    b = xpx.atleast_nd(b, ndim=1, xp=xp)

    try:
        wo = float(wo)
    except TypeError:
        wo = float(wo[0])
    d = a.shape[0]
    n = b.shape[0]
    M = max((d, n))
    pwo = wo ** xp.arange(M - 1, -1, -1, dtype=xp.float64)
    start1 = max((n - d, 0))
    start2 = max((d - n, 0))
    b = b * pwo[start1] / pwo[start2:]
    a = a * pwo[start1] / pwo[start1:]
    return normalize(b, a)

