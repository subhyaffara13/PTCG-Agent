
def freqz_zpk(z, p, k, worN=512, whole=False, fs=2*pi):
    r"""
    Compute the frequency response of a digital filter in ZPK form.

    Given the Zeros, Poles and Gain of a digital filter, compute its frequency
    response:

    :math:`H(z)=k \prod_i (z - Z[i]) / \prod_j (z - P[j])`

    where :math:`k` is the `gain`, :math:`Z` are the `zeros` and :math:`P` are
    the `poles`.

    Parameters
    ----------
    z : array_like
        Zeroes of a linear filter
    p : array_like
        Poles of a linear filter
    k : scalar
        Gain of a linear filter
    worN : {None, int, array_like}, optional
        If a single integer, then compute at that many frequencies (default is
        N=512).

        If an array_like, compute the response at the frequencies given.
        These are in the same units as `fs`.
    whole : bool, optional
        Normally, frequencies are computed from 0 to the Nyquist frequency,
        fs/2 (upper-half of unit-circle). If `whole` is True, compute
        frequencies from 0 to fs. Ignored if w is array_like.
    fs : float, optional
        The sampling frequency of the digital system. Defaults to 2*pi
        radians/sample (so w is from 0 to pi).

        .. versionadded:: 1.2.0

    Returns
    -------
    w : ndarray
        The frequencies at which `h` was computed, in the same units as `fs`.
        By default, `w` is normalized to the range [0, pi) (radians/sample).
    h : ndarray
        The frequency response, as complex numbers.

    See Also
    --------
    freqs : Compute the frequency response of an analog filter in TF form
    freqs_zpk : Compute the frequency response of an analog filter in ZPK form
    freqz : Compute the frequency response of a digital filter in TF form

    Notes
    -----
    .. versionadded:: 0.19.0

    Examples
    --------
    Design a 4th-order digital Butterworth filter with cut-off of 100 Hz in a
    system with sample rate of 1000 Hz, and plot the frequency response:

    >>> import numpy as np
    >>> from scipy import signal
    >>> z, p, k = signal.butter(4, 100, output='zpk', fs=1000)
    >>> w, h = signal.freqz_zpk(z, p, k, fs=1000)

    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> ax1 = fig.add_subplot(1, 1, 1)
    >>> ax1.set_title('Digital filter frequency response')

    >>> ax1.plot(w, 20 * np.log10(abs(h)), 'b')
    >>> ax1.set_ylabel('Amplitude [dB]', color='b')
    >>> ax1.set_xlabel('Frequency [Hz]')
    >>> ax1.grid(True)

    >>> ax2 = ax1.twinx()
    >>> phase = np.unwrap(np.angle(h))
    >>> ax2.plot(w, phase, 'g')
    >>> ax2.set_ylabel('Phase [rad]', color='g')

    >>> plt.axis('tight')
    >>> plt.show()

    """
    xp = array_namespace(z, p)
    z, p = map(xp.asarray, (z, p))

    z = xpx.atleast_nd(z, ndim=1, xp=xp)
    p = xpx.atleast_nd(p, ndim=1, xp=xp)
    res_dtype = xp.result_type(z, p)
    res_dtype = xp.float64 if res_dtype in (xp.float64, xp.complex128) else xp.float32

    fs = _validate_fs(fs, allow_none=False)

    if whole:
        lastpoint = 2 * pi
    else:
        lastpoint = pi

    if worN is None:
        # For backwards compatibility
        w = xp.linspace(0, lastpoint, 512, endpoint=False, dtype=res_dtype)
    elif _is_int_type(worN):
        w = xp.linspace(0, lastpoint, worN, endpoint=False, dtype=res_dtype)
    else:
        w = xp.asarray(worN)
        if xp.isdtype(w.dtype, 'integral'):
            w = xp.astype(w, xp_default_dtype(xp))
        w = xpx.atleast_nd(w, ndim=1, xp=xp)
        w = 2 * pi * w / fs

    zm1 = xp.exp(1j * w)
    func = _pu.npp_polyvalfromroots
    h = xp.asarray(k, dtype=res_dtype) * func(zm1, z, xp=xp) / func(zm1, p, xp=xp)

    w = w*(fs/(2*pi))

    return w, h

