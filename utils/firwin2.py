
def firwin2(numtaps, freq, gain, *, nfreqs=None, window='hamming',
            antisymmetric=False, fs=None):
    """
    FIR filter design using the window method.

    From the given frequencies `freq` and corresponding gains `gain`,
    this function constructs an FIR filter with linear phase and
    (approximately) the given frequency response.

    Parameters
    ----------
    numtaps : int
        The number of taps in the FIR filter.  `numtaps` must be less than
        `nfreqs`.
    freq : array_like, 1-D
        The frequency sampling points. Typically 0.0 to 1.0 with 1.0 being
        Nyquist.  The Nyquist frequency is half `fs`.
        The values in `freq` must be nondecreasing. A value can be repeated
        once to implement a discontinuity. The first value in `freq` must
        be 0, and the last value must be ``fs/2``. Values 0 and ``fs/2`` must
        not be repeated.
    gain : array_like
        The filter gains at the frequency sampling points. Certain
        constraints to gain values, depending on the filter type, are applied,
        see Notes for details.
    nfreqs : int, optional
        The size of the interpolation mesh used to construct the filter.
        For most efficient behavior, this should be a power of 2 plus 1
        (e.g, 129, 257, etc). The default is one more than the smallest
        power of 2 that is not less than `numtaps`. `nfreqs` must be greater
        than `numtaps`.
    window : str or (str, float) or float, or None, optional
        Desired window to use. Default is ``'hamming'``. The window will be symmetric,
        unless a suffix ``'_periodic'`` is appended to the window name (e.g.,
        ``'hamming_perodic'``) Consult `~scipy.signal.get_window` for a list of windows
        and required parameters. If ``None``, no window function is applied.
    antisymmetric : bool, optional
        Whether resulting impulse response is symmetric/antisymmetric.
        See Notes for more details.
    fs : float, optional
        The sampling frequency of the signal. Each frequency in `cutoff`
        must be between 0 and ``fs/2``. Default is 2.

    Returns
    -------
    taps : ndarray
        The filter coefficients of the FIR filter, as a 1-D array of length
        `numtaps`.

    See Also
    --------
    firls
    firwin
    minimum_phase
    remez

    Notes
    -----
    From the given set of frequencies and gains, the desired response is
    constructed in the frequency domain. The inverse FFT is applied to the
    desired response to create the associated convolution kernel, and the
    first `numtaps` coefficients of this kernel, scaled by `window`, are
    returned.

    The FIR filter will have linear phase. The type of filter is determined by
    the value of 'numtaps` and `antisymmetric` flag.
    There are four possible combinations:

       - odd  `numtaps`, `antisymmetric` is False, type I filter is produced
       - even `numtaps`, `antisymmetric` is False, type II filter is produced
       - odd  `numtaps`, `antisymmetric` is True, type III filter is produced
       - even `numtaps`, `antisymmetric` is True, type IV filter is produced

    Magnitude response of all but type I filters are subjects to following
    constraints:

       - type II  -- zero at the Nyquist frequency
       - type III -- zero at zero and Nyquist frequencies
       - type IV  -- zero at zero frequency

    .. versionadded:: 0.9.0

    References
    ----------
    .. [1] Oppenheim, A. V. and Schafer, R. W., "Discrete-Time Signal
       Processing", Prentice-Hall, Englewood Cliffs, New Jersey (1989).
       (See, for example, Section 7.4.)

    .. [2] Smith, Steven W., "The Scientist and Engineer's Guide to Digital
       Signal Processing", Ch. 17. http://www.dspguide.com/ch17/1.htm

    Examples
    --------
    A lowpass FIR filter with a response that is 1 on [0.0, 0.5], and
    that decreases linearly on [0.5, 1.0] from 1 to 0:

    >>> from scipy import signal
    >>> taps = signal.firwin2(150, [0.0, 0.5, 1.0], [1.0, 1.0, 0.0])
    >>> print(taps[72:78])
    [-0.02286961 -0.06362756  0.57310236  0.57310236 -0.06362756 -0.02286961]

    """
    xp = array_namespace(freq, gain)
    freq, gain = xp.asarray(freq), xp.asarray(gain)

    fs = _validate_fs(fs, allow_none=True)
    fs = 2 if fs is None else fs
    nyq = 0.5 * fs

    if freq.shape[0] != gain.shape[0]:
        raise ValueError('freq and gain must be of same length.')

    if nfreqs is not None and numtaps >= nfreqs:
        raise ValueError(
            f'ntaps must be less than nfreqs, but firwin2 was called with '
            f'ntaps={numtaps} and nfreqs={nfreqs}'
        )

    if freq[0] != 0 or freq[-1] != nyq:
        raise ValueError('freq must start with 0 and end with fs/2.')
    d = freq[1:] - freq[:-1]
    if xp.any(d < 0):
        raise ValueError('The values in freq must be nondecreasing.')
    d2 = d[:-1] + d[1:]
    if xp.any(d2 == 0):
        raise ValueError('A value in freq must not occur more than twice.')
    if freq[1] == 0:
        raise ValueError('Value 0 must not be repeated in freq')
    if freq[-2] == nyq:
        raise ValueError('Value fs/2 must not be repeated in freq')

    if antisymmetric:
        if numtaps % 2 == 0:
            ftype = 4
        else:
            ftype = 3
    else:
        if numtaps % 2 == 0:
            ftype = 2
        else:
            ftype = 1

    if ftype == 2 and gain[-1] != 0.0:
        raise ValueError("A Type II filter must have zero gain at the "
                         "Nyquist frequency.")
    elif ftype == 3 and (gain[0] != 0.0 or gain[-1] != 0.0):
        raise ValueError("A Type III filter must have zero gain at zero "
                         "and Nyquist frequencies.")
    elif ftype == 4 and gain[0] != 0.0:
        raise ValueError("A Type IV filter must have zero gain at zero "
                         "frequency.")

    if nfreqs is None:
        nfreqs = 1 + 2 ** int(ceil(log(numtaps, 2)))

    if xp.any(d == 0):
        # Tweak any repeated values in freq so that interp works.
        freq = xp.asarray(freq, copy=True)
        eps = xp.finfo(xp_default_dtype(xp)).eps * nyq
        for k in range(freq.shape[0] - 1):
            if freq[k] == freq[k + 1]:
                freq[k] = freq[k] - eps
                freq[k + 1] = freq[k + 1] + eps
        # Check if freq is strictly increasing after tweak
        d = freq[1:] - freq[:-1]
        if xp.any(d <= 0):
            raise ValueError("freq cannot contain numbers that are too close "
                             "(within eps * (fs/2): "
                             f"{eps}) to a repeated value")

    # Linearly interpolate the desired response on a uniform mesh `x`.
    x = np.linspace(0.0, nyq, nfreqs)
    fx = np.interp(x, np.asarray(freq), np.asarray(gain))  # XXX array-api-extra#193
    x = xp.asarray(x)
    fx = xp.asarray(fx)

    # Adjust the phases of the coefficients so that the first `ntaps` of the
    # inverse FFT are the desired filter coefficients.
    shift = xp.exp(-(numtaps - 1) / 2. * 1j * xp.pi * x / nyq)
    if ftype > 2:
        shift *= 1j

    fx2 = fx * shift

    # Use irfft to compute the inverse FFT.
    out_full = irfft(fx2)

    if window is not None:
        # Create the window to apply to the filter coefficients.
        wind = get_window(window, numtaps, fftbins=False, xp=xp)
    else:
        wind = 1

    # Keep only the first `numtaps` coefficients in `out`, and multiply by
    # the window.
    out = out_full[:numtaps] * wind

    if ftype == 3:
        out[xp_size(out) // 2] = 0.0

    return out

