
def lp2hp(b, a, wo=1.0):
    r"""
    Transform a lowpass filter prototype to a highpass filter.

    Return an analog high-pass filter with cutoff frequency `wo`
    from an analog low-pass filter prototype with unity cutoff frequency, in
    transfer function ('ba') representation.

    Parameters
    ----------
    b : array_like, shape (M,)
        Numerator polynomial coefficients. Must be 1-D.
    a : array_like, shape (N,)
        Denominator polynomial coefficients. Must be 1-D.
    wo : float
        Desired cutoff, as angular frequency (e.g., rad/s).
        Defaults to no change.

    Returns
    -------
    b : array_like
        Numerator polynomial coefficients of the transformed high-pass filter.
    a : array_like
        Denominator polynomial coefficients of the transformed high-pass filter.

    See Also
    --------
    lp2lp, lp2bp, lp2bs, bilinear
    lp2hp_zpk

    Notes
    -----
    This is derived from the s-plane substitution

    .. math:: s \rightarrow \frac{\omega_0}{s}

    This maintains symmetry of the lowpass and highpass responses on a
    logarithmic scale.

    Examples
    --------
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt

    >>> lp = signal.lti([1.0], [1.0, 1.0])
    >>> hp = signal.lti(*signal.lp2hp(lp.num, lp.den))
    >>> w, mag_lp, p_lp = lp.bode()
    >>> w, mag_hp, p_hp = hp.bode(w)

    >>> plt.plot(w, mag_lp, label='Lowpass')
    >>> plt.plot(w, mag_hp, label='Highpass')
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
    if wo != 1:
        pwo = wo ** xp.arange(max((d, n)), dtype=b.dtype)
    else:
        pwo = xp.ones(max((d, n)), dtype=b.dtype)
    if d >= n:
        outa = xp.flip(a) * pwo
        outb = _resize(b, (d,), xp=xp)
        outb = xpx.at(outb)[n:].set(0.0)
        outb = xpx.at(outb)[:n].set(xp.flip(b) * pwo[:n])
    else:
        outb = xp.flip(b) * pwo
        outa = _resize(a, (n,), xp=xp)
        outa = xpx.at(outa)[d:].set(0.0)
        outa = xpx.at(outa)[:d].set(xp.flip(a) * pwo[:d])

    return normalize(outb, outa)

