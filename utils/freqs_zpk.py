
def freqs_zpk(z, p, k, worN=200):
    """
    Compute frequency response of analog filter.

    Given the zeros `z`, poles `p`, and gain `k` of a filter, compute its
    frequency response::

                (jw-z[0]) * (jw-z[1]) * ... * (jw-z[-1])
     H(w) = k * ----------------------------------------
                (jw-p[0]) * (jw-p[1]) * ... * (jw-p[-1])

    Parameters
    ----------
    z : array_like
        Zeroes of a linear filter
    p : array_like
        Poles of a linear filter
    k : scalar
        Gain of a linear filter
    worN : {None, int, array_like}, optional
        If None, then compute at 200 frequencies around the interesting parts
        of the response curve (determined by pole-zero locations). If a single
        integer, then compute at that many frequencies. Otherwise, compute the
        response at the angular frequencies (e.g., rad/s) given in `worN`.

    Returns
    -------
    w : ndarray
        The angular frequencies at which `h` was computed.
    h : ndarray
        The frequency response.

    See Also
    --------
    freqs : Compute the frequency response of an analog filter in TF form
    freqz : Compute the frequency response of a digital filter in TF form
    freqz_zpk : Compute the frequency response of a digital filter in ZPK form

    Notes
    -----
    .. versionadded:: 0.19.0

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.signal import freqs_zpk, iirfilter

    >>> z, p, k = iirfilter(4, [1, 10], 1, 60, analog=True, ftype='cheby1',
    ...                     output='zpk')

    >>> w, h = freqs_zpk(z, p, k, worN=np.logspace(-1, 2, 1000))

    >>> import matplotlib.pyplot as plt
    >>> plt.semilogx(w, 20 * np.log10(abs(h)))
    >>> plt.xlabel('Frequency [rad/s]')
    >>> plt.ylabel('Amplitude response [dB]')
    >>> plt.grid(True)
    >>> plt.show()

    """
    xp = array_namespace(z, p)
    z, p = map(xp.asarray, (z, p))

    # NB: k is documented to be a scalar; for backwards compat we keep allowing it
    # to be a size-1 array, but it does not influence the namespace calculation.
    k = xp.asarray(k, dtype=xp_default_dtype(xp))
    if xp_size(k) > 1:
        raise ValueError('k must be a single scalar gain')

    if worN is None:
        # For backwards compatibility
        w = findfreqs(z, p, 200, kind='zp')
    elif _is_int_type(worN):
        w = findfreqs(z, p, worN, kind='zp')
    else:
        w = worN

    w = xpx.atleast_nd(xp.asarray(w), ndim=1, xp=xp)
    s = 1j * w
    num = _pu.npp_polyvalfromroots(s, z, xp=xp)
    den = _pu.npp_polyvalfromroots(s, p, xp=xp)
    h = k * num/den
    return w, h

