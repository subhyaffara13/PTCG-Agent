
def lp2lp_zpk(z, p, k, wo=1.0):
    r"""
    Transform a lowpass filter prototype to a different frequency.

    Return an analog low-pass filter with cutoff frequency `wo`
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
        Zeros of the transformed low-pass filter transfer function.
    p : ndarray
        Poles of the transformed low-pass filter transfer function.
    k : float
        System gain of the transformed low-pass filter.

    See Also
    --------
    lp2hp_zpk, lp2bp_zpk, lp2bs_zpk, bilinear
    lp2lp

    Notes
    -----
    This is derived from the s-plane substitution

    .. math:: s \rightarrow \frac{s}{\omega_0}

    .. versionadded:: 1.1.0

    Examples
    --------
    Use the 'zpk' (Zero-Pole-Gain) representation of a lowpass filter to
    transform it to a new 'zpk' representation associated with a cutoff frequency wo.

    >>> from scipy.signal import lp2lp_zpk
    >>> z   = [7,   2]
    >>> p   = [5,   13]
    >>> k   = 0.8
    >>> wo  = 0.4
    >>> lp2lp_zpk(z, p, k, wo)
    (   array([2.8, 0.8]), array([2. , 5.2]), 0.8)
    """
    xp = array_namespace(z, p)

    z, p = map(xp.asarray, (z, p))
    z = xpx.atleast_nd(z, ndim=1, xp=xp)
    p = xpx.atleast_nd(p, ndim=1, xp=xp)

    wo = float(wo)  # Avoid int wraparound

    degree = _relative_degree(z, p)

    # Scale all points radially from origin to shift cutoff frequency
    z_lp = wo * z
    p_lp = wo * p

    # Each shifted pole decreases gain by wo, each shifted zero increases it.
    # Cancel out the net change to keep overall gain the same
    k_lp = k * wo**degree

    return z_lp, p_lp, k_lp

