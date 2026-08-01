
def lp2bp_zpk(z, p, k, wo=1.0, bw=1.0):
    r"""
    Transform a lowpass filter prototype to a bandpass filter.

    Return an analog band-pass filter with center frequency `wo` and
    bandwidth `bw` from an analog low-pass filter prototype with unity
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
        Desired passband center, as angular frequency (e.g., rad/s).
        Defaults to no change.
    bw : float
        Desired passband width, as angular frequency (e.g., rad/s).
        Defaults to 1.

    Returns
    -------
    z : ndarray
        Zeros of the transformed band-pass filter transfer function.
    p : ndarray
        Poles of the transformed band-pass filter transfer function.
    k : float
        System gain of the transformed band-pass filter.

    See Also
    --------
    lp2lp_zpk, lp2hp_zpk, lp2bs_zpk, bilinear
    lp2bp

    Notes
    -----
    This is derived from the s-plane substitution

    .. math:: s \rightarrow \frac{s^2 + {\omega_0}^2}{s \cdot \mathrm{BW}}

    This is the "wideband" transformation, producing a passband with
    geometric (log frequency) symmetry about `wo`.

    .. versionadded:: 1.1.0

    Examples
    --------
    Use the 'zpk' (Zero-Pole-Gain) representation of a lowpass filter to
    transform it to a bandpass filter with a center frequency wo and
    bandwidth bw.

    >>> from scipy.signal import lp2bp_zpk
    >>> z   = [ 5 + 2j ,  5 - 2j ]
    >>> p   = [ 7      ,  -16    ]
    >>> k   = 0.8
    >>> wo  = 0.62
    >>> bw  = 15
    >>> lp2bp_zpk(z, p, k, wo, bw)
    (   array([7.49955815e+01+3.00017676e+01j, 7.49955815e+01-3.00017676e+01j,
               4.41850748e-03-1.76761126e-03j, 4.41850748e-03+1.76761126e-03j]),
        array([1.04996339e+02+0.j, -1.60167736e-03+0.j,  3.66108003e-03+0.j,
               -2.39998398e+02+0.j]), 0.8)
    """
    xp = array_namespace(z, p)

    z, p = map(xp.asarray, (z, p))
    z, p = xp_promote(z, p, force_floating=True, xp=xp)
    z = xpx.atleast_nd(z, ndim=1, xp=xp)
    p = xpx.atleast_nd(p, ndim=1, xp=xp)

    wo = float(wo)
    bw = float(bw)

    degree = _relative_degree(z, p)

    # Scale poles and zeros to desired bandwidth
    z_lp = z * bw/2
    p_lp = p * bw/2

    # Square root needs to produce complex result, not NaN
    z_lp = xp.astype(z_lp, xp.complex128)
    p_lp = xp.astype(p_lp, xp.complex128)

    # Duplicate poles and zeros and shift from baseband to +wo and -wo
    z_bp = xp.concat((z_lp + xp.sqrt(z_lp**2 - wo**2),
                      z_lp - xp.sqrt(z_lp**2 - wo**2)))
    p_bp = xp.concat((p_lp + xp.sqrt(p_lp**2 - wo**2),
                      p_lp - xp.sqrt(p_lp**2 - wo**2)))

    # Move degree zeros to origin, leaving degree zeros at infinity for BPF
    z_bp = xp.concat((z_bp, xp.zeros(degree)))

    # Cancel out gain change from frequency scaling
    k_bp = k * bw**degree

    return z_bp, p_bp, k_bp

