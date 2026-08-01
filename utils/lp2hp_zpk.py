
def lp2hp_zpk(z, p, k, wo=1.0):
    r"""
    Transform a lowpass filter prototype to a highpass filter.

    Return an analog high-pass filter with cutoff frequency `wo`
    from an analog low-pass filter prototype with unity cutoff frequency,
    using zeros, poles, and gain ('zpk') representation.

    Parameters
    ----------
    z : array_like
        Zeros of the analog filter transfer function.
    p : array_like
        Poles of the analog filter transfer function.
    k : float
        System gain of the analog filter transfer function.
    wo : float
        Desired cutoff, as angular frequency (e.g., rad/s).
        Defaults to no change.

    Returns
    -------
    z : ndarray
        Zeros of the transformed high-pass filter transfer function.
    p : ndarray
        Poles of the transformed high-pass filter transfer function.
    k : float
        System gain of the transformed high-pass filter.

    See Also
    --------
    lp2lp_zpk, lp2bp_zpk, lp2bs_zpk, bilinear
    lp2hp

    Notes
    -----
    This is derived from the s-plane substitution

    .. math:: s \rightarrow \frac{\omega_0}{s}

    This maintains symmetry of the lowpass and highpass responses on a
    logarithmic scale.

    .. versionadded:: 1.1.0

    Examples
    --------
    Use the 'zpk' (Zero-Pole-Gain) representation of a lowpass filter to
    transform it to a highpass filter with a cutoff frequency wo.

    >>> from scipy.signal import lp2hp_zpk
    >>> z   = [ -2 + 3j ,  -0.5 - 0.8j ]
    >>> p   = [ -1      ,  -4          ]
    >>> k   = 10
    >>> wo  = 0.6
    >>> lp2hp_zpk(z, p, k, wo)
    (   array([-0.09230769-0.13846154j, -0.33707865+0.53932584j]),
        array([-0.6 , -0.15]),
        8.5)
    """
    xp = array_namespace(z, p)

    z, p = map(xp.asarray, (z, p))
    # XXX: no xp_promote here since that breaks TestButter
    z = xpx.atleast_nd(z, ndim=1, xp=xp)
    p = xpx.atleast_nd(p, ndim=1, xp=xp)

    wo = float(wo)

    degree = _relative_degree(z, p)

    # Invert positions radially about unit circle to convert LPF to HPF
    # Scale all points radially from origin to shift cutoff frequency
    z_hp = wo / z
    p_hp = wo / p

    # If lowpass had zeros at infinity, inverting moves them to origin.
    z_hp = xp.concat((z_hp, xp.zeros(degree)))

    # Cancel out gain change caused by inversion
    k_hp = k * xp.real(xp.prod(-z) / xp.prod(-p))

    return z_hp, p_hp, k_hp

