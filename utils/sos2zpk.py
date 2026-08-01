
def sos2zpk(sos):
    """
    Return zeros, poles, and gain of a series of second-order sections.

    Parameters
    ----------
    sos : array_like
        Array of second-order filter coefficients, must have shape
        ``(n_sections, 6)``. See `sosfilt` for the SOS filter format
        specification.

    Returns
    -------
    z : ndarray
        Zeros of the transfer function.
    p : ndarray
        Poles of the transfer function.
    k : float
        System gain.

    Notes
    -----
    The number of zeros and poles returned will be ``n_sections * 2``
    even if some of these are (effectively) zero.

    .. versionadded:: 0.16.0
    """
    xp = array_namespace(sos)
    sos = xp.asarray(sos)

    n_sections = sos.shape[0]
    z = xp.zeros(n_sections*2, dtype=xp.complex128)
    p = xp.zeros(n_sections*2, dtype=xp.complex128)
    k = 1.
    for section in range(n_sections):
        zpk = tf2zpk(sos[section, :3], sos[section, 3:])
        z = xpx.at(z, slice(2*section, 2*section + zpk[0].shape[0])).set(zpk[0])
        p = xpx.at(p, slice(2*section, 2*section + zpk[1].shape[0])).set(zpk[1])
        k *= zpk[2]
    return z, p, k

