
def lp2bs_zpk(z, p, k, wo=1.0, bw=1.0):
    r"""
    Transform a lowpass filter prototype to a bandstop filter.

    Return an analog band-stop filter with center frequency `wo` and
    stopband width `bw` from an analog low-pass filter prototype with unity
    cutoff frequency, using zeros, poles, and gain ('zpk') representation.

    Parameters
    ----------
    z : array_like
        Zeros of the analog filter transfer function.
    p : array_like
        Poles of the analog filter transfer function.
    k : float
        System gain of the analog filter transfer function.
    wo : float
        Desired stopband center, as angular frequency (e.g., rad/s).
        Defaults to no change.
    bw : float
        Desired stopband width, as angular frequency (e.g., rad/s).
        Defaults to 1.

    Returns
    -------
    z : ndarray
        Zeros of the transformed band-stop filter transfer function.
    p : ndarray
        Poles of the transformed band-stop filter transfer function.
    k : float
        System gain of the transformed band-stop filter.

    See Also
    --------
    lp2lp_zpk, lp2hp_zpk, lp2bp_zpk, bilinear
    lp2bs

    Notes
    -----
    This is derived from the s-plane substitution

    .. math:: s \rightarrow \frac{s \cdot \mathrm{BW}}{s^2 + {\omega_0}^2}

    This is the "wideband" transformation, producing a stopband with
    geometric (log frequency) symmetry about `wo`.

    .. versionadded:: 1.1.0

    Examples
    --------
    Transform a low-pass filter represented in 'zpk' (Zero-Pole-Gain) form
    into a bandstop filter represented in 'zpk' form, with a center frequency wo and
    bandwidth bw.

    >>> from scipy.signal import lp2bs_zpk
    >>> z   = [             ]
    >>> p   = [ 0.7 ,    -1 ]
    >>> k   = 9
    >>> wo  = 0.5
    >>> bw  = 10
    >>> lp2bs_zpk(z, p, k, wo, bw)
    (   array([0.+0.5j, 0.+0.5j, 0.-0.5j, 0.-0.5j]),
        array([14.2681928 +0.j, -0.02506281+0.j,  0.01752149+0.j, -9.97493719+0.j]),
        -12.857142857142858)
    """
    xp = array_namespace(z, p)

    z, p = map(xp.asarray, (z, p))
    z, p = xp_promote(z, p, force_floating=True, xp=xp)
    z = xpx.atleast_nd(z, ndim=1, xp=xp)
    p = xpx.atleast_nd(p, ndim=1, xp=xp)

    wo = float(wo)
    bw = float(bw)

    degree = _relative_degree(z, p)

    # Invert to a highpass filter with desired bandwidth
    z_hp = (bw/2) / z
    p_hp = (bw/2) / p

    # Square root needs to produce complex result, not NaN
    z_hp = xp.astype(z_hp, xp.complex128)
    p_hp = xp.astype(p_hp, xp.complex128)

    # Duplicate poles and zeros and shift from baseband to +wo and -wo
    z_bs = xp.concat((z_hp + xp.sqrt(z_hp**2 - wo**2),
                      z_hp - xp.sqrt(z_hp**2 - wo**2)))
    p_bs = xp.concat((p_hp + xp.sqrt(p_hp**2 - wo**2),
                      p_hp - xp.sqrt(p_hp**2 - wo**2)))

    # Move any zeros that were at infinity to the center of the stopband
    z_bs = xp.concat((z_bs, xp.full(degree, +1j*wo)))
    z_bs = xp.concat((z_bs, xp.full(degree, -1j*wo)))

    # Cancel out gain change caused by inversion
    k_bs = k * xp.real(xp.prod(-z) / xp.prod(-p))

    return z_bs, p_bs, k_bs

