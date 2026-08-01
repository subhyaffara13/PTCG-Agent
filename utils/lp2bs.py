
def lp2bs(b, a, wo=1.0, bw=1.0):
    r"""
    Transform a lowpass filter prototype to a bandstop filter.

    Return an analog band-stop filter with center frequency `wo` and
    bandwidth `bw` from an analog low-pass filter prototype with unity
    cutoff frequency, in transfer function ('ba') representation.

    Parameters
    ----------
    b : array_like, shape (M,)
        Numerator polynomial coefficients. Must be 1-D.
    a : array_like, shape (N,)
        Denominator polynomial coefficients. Must be 1-D.
    wo : float
        Desired stopband center, as angular frequency (e.g., rad/s).
        Defaults to no change.
    bw : float
        Desired stopband width, as angular frequency (e.g., rad/s).
        Defaults to 1.

    Returns
    -------
    b : array_like
        Numerator polynomial coefficients of the transformed band-stop filter.
    a : array_like
        Denominator polynomial coefficients of the transformed band-stop filter.

    See Also
    --------
    lp2lp, lp2hp, lp2bp, bilinear
    lp2bs_zpk

    Notes
    -----
    This is derived from the s-plane substitution

    .. math:: s \rightarrow \frac{s \cdot \mathrm{BW}}{s^2 + {\omega_0}^2}

    This is the "wideband" transformation, producing a stopband with
    geometric (log frequency) symmetry about `wo`.

    Examples
    --------
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt

    >>> lp = signal.lti([1.0], [1.0, 1.5])
    >>> bs = signal.lti(*signal.lp2bs(lp.num, lp.den))
    >>> w, mag_lp, p_lp = lp.bode()
    >>> w, mag_bs, p_bs = bs.bode(w)
    >>> plt.plot(w, mag_lp, label='Lowpass')
    >>> plt.plot(w, mag_bs, label='Bandstop')
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

    D = a.shape[0] - 1
    N = b.shape[0] - 1
    M = max([N, D])
    Np = M + M
    Dp = M + M
    bprime = xp.empty(Np + 1, dtype=b.dtype)
    aprime = xp.empty(Dp + 1, dtype=a.dtype)
    wosq = wo * wo
    for j in range(Np + 1):
        val = 0.0
        for i in range(0, N + 1):
            for k in range(0, M - i + 1):
                if i + 2 * k == j:
                    val += (comb(M - i, k) * b[N - i] *
                            (wosq) ** (M - i - k) * bw ** i)
        bprime = xpx.at(bprime, Np - j).set(val, xp=xp)
    for j in range(Dp + 1):
        val = 0.0
        for i in range(0, D + 1):
            for k in range(0, M - i + 1):
                if i + 2 * k == j:
                    val += (comb(M - i, k) * a[D - i] *
                            (wosq) ** (M - i - k) * bw ** i)
        aprime = xpx.at(aprime, Dp - j).set(val, xp=xp)

    return normalize(bprime, aprime)

