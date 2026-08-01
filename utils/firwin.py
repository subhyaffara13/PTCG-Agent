
def firwin(numtaps, cutoff, *, width=None, window='hamming', pass_zero=True,
           scale=True, fs=None):
    r"""FIR filter design using the window method.

    This function computes the coefficients of a finite impulse response
    filter. The filter will have linear phase; it will be Type I if
    `numtaps` is odd and Type II if `numtaps` is even.

    Type II filters always have zero response at the Nyquist frequency, so a
    ValueError exception is raised if firwin is called with `numtaps` even and
    having a passband whose right end is at the Nyquist frequency.

    Parameters
    ----------
    numtaps : int
        Length of the filter (number of coefficients, i.e., the filter
        order + 1).  `numtaps` must be odd if a passband includes the
        Nyquist frequency.
    cutoff : float or 1-D array_like
        Cutoff frequency of filter (expressed in the same units as `fs`)
        or an array of cutoff frequencies (that is, band edges). In the
        former case, as a float, the cutoff frequency should correspond
        with the half-amplitude point, where the attenuation will be -6 dB.
        In the latter case, the frequencies in `cutoff` should be positive
        and monotonically increasing between 0 and `fs/2`. The values 0
        and `fs/2` must not be included in `cutoff`. It should be noted
        that this is different from the behavior of `~scipy.signal.iirdesign`,
        where the cutoff is the half-power point (-3 dB).
    width : float or None, optional
        If not ``None``, then a `~scipy.signal.windows.kaiser` window is calculated
        where `width` specifies the approximate width of the transition region
        (expressed in the same unit as `fs`). This is achieved by utilizing
        `~scipy.signal.kaiser_atten` to calculate an attenuation which is passed to
        `~scipy.signal.kaiser_beta` for determining the β parameter for the kaiser
        window. In this case, the `window` argument is ignored.
    window : str or tuple of str and parameter values, optional
        Desired window to use. Default is ``'hamming'``. The window will be symmetric,
        unless a suffix ``'_periodic'`` is appended to the window name (e.g.,
        ``'hamming_perodic'``) Consult `~scipy.signal.get_window` for a list of windows
        and required parameters.
    pass_zero : {True, False, 'bandpass', 'lowpass', 'highpass', 'bandstop'}, optional
        Toggles the zero frequency bin (or DC gain) to be in the passband (``True``) or
        in the stopband (``False``).  ``'bandstop'``, ``'lowpass'`` are synonyms for
        ``True`` and ``'bandpass'``, ``'highpass'`` are synonyms for ``False``.
        ``'lowpass'``, ``'highpass'`` additionally require `cutoff` to be a scalar
        value or a length-one array. Default: ``True``.

        .. versionadded:: 1.3.0
           Support for string arguments.
    scale : bool, optional
        Set to ``True`` to scale the coefficients so that the frequency response is
        exactly unity at a certain frequency. That frequency is either:

        - 0 (DC) if the first passband starts at 0 (i.e., `pass_zero` is ``True``)
        - `fs/2` (the Nyquist frequency) if the first passband ends at `fs/2`
          (i.e., the filter is a single band highpass filter); center of first
          passband otherwise

    fs : float, optional
        The sampling frequency of the signal. Each frequency in `cutoff`
        must be between 0 and ``fs/2``.  Default is 2.

    Returns
    -------
    h : ndarray
        FIR filter coefficients as 1d array with `numtaps` entries.

    Raises
    ------
    ValueError
        If any value in `cutoff` is less than or equal to 0 or greater
        than or equal to ``fs/2``, if the values in `cutoff` are not strictly
        monotonically increasing, or if `numtaps` is even but a passband
        includes the Nyquist frequency.

    See Also
    --------
    firwin2:  Window method FIR filter design specifying gain-frequency pairs.
    firwin_2d: 2D FIR filter design using the window method.
    firls: FIR filter design using least-squares error minimization.
    minimum_phase: Convert a FIR filter to minimum phase
    remez: Calculate the minimax optimal filter using the Remez exchange algorithm.

    Examples
    --------
    The following example calculates frequency responses of a 30 Hz low-pass filter
    with various numbers of taps. The transition region width is 20 Hz. The upper plot
    shows the gain and the lower plot the phase. The vertical dashed line marks the
    corner frequency and the gray background the transition region.

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> import scipy.signal as signal
    ...
    >>> fs = 200  # sampling frequency and number of taps
    >>> f_c, width = 30, 20  # corner frequency (-6 dB gain)
    >>> taps = [20, 40, 60]  # number of taps
    ...
    >>> fg, (ax0, ax1) = plt.subplots(2, 1, sharex='all', layout="constrained",
    ...                               figsize=(5, 4))
    >>> ax0.set_title(rf"Response of ${f_c}\,$Hz low-pass Filter with " +
    ...               rf"${width}\,$Hz transition region")
    >>> ax0.set(ylabel="Gain in dB", xlim=(0, fs/2))
    >>> ax1.set(xlabel=rf"Frequency $f\,$ in hertz (sampling frequency $f_S={fs}\,$Hz)",
    ...         ylabel="Phase in Degrees")
    ...
    >>> for n in taps:  # calculate filter and plot response:
    ...     bb = signal.firwin(n, f_c, width=width, fs=fs)
    ...     f, H = signal.freqz(bb, fs=fs)  # calculate frequency response
    ...     H_dB, H_ph = 20 * np.log10(abs(H)), np.rad2deg(np.unwrap(np.angle(H)))
    ...     H_ph[H_dB<-150] = np.nan
    ...     ax0.plot(f, H_dB, alpha=.5, label=rf"{n} taps")
    ...     ax1.plot(f, H_ph, alpha=.5, label=rf"{n} taps")
    >>> for ax_ in (ax0, ax1):
    ...     ax_.axvspan(f_c-width/2, f_c+width/2,color='gray', alpha=.25)
    ...     ax_.axvline(f_c, color='gray', linestyle='--', alpha=.5)
    ...     ax_.grid()
    ...     ax_.legend()
    >>> plt.show()

    The plots show that with increasing number of taps, the suppression in the stopband
    increases and the (negative) slope of the phase steepens, which signifies a longer
    signal delay in the filter. Note that the plots contain numeric artifacts caused by
    the limited frequency resolution: The phase jumps are not real---in reality the
    phase is a straight line with a constant negative slope. Furthermore, the gains
    contain zero values (i.e., -∞ dB), which are also not depicted.

    The second example determines the frequency responses of a 30 Hz low-pass filter
    with 40 taps. This time the width of the transition region varies:

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> import scipy.signal as signal
    ...
    >>> fs = 200  # sampling frequency and number of taps
    >>> n, f_c = 40, 30  # number of taps and corner frequency (-6 dB gain)
    >>> widths = (2, 10, 25)  # width of transition region
    ...
    >>> fg, ax = plt.subplots(1, 1, layout="constrained",)
    >>> ax.set(title=rf"Response of {n}-tap ${f_c}\,$Hz low-pass Filter",
    ...        xlabel=rf"Frequency $f\,$ in hertz (sampling frequency $f_S={fs}\,$Hz)",
    ...        ylabel="Gain in dB", xlim=(0, fs/2))
    >>> ax.axvline(f_c, color='gray', linestyle='--', alpha=.7)  # mark corner frequency
    ...
    >>> for width in widths:  # calculate filter and plot response:
    ...     bb = signal.firwin(n, f_c, width=width, fs=fs)
    ...     f, H = signal.freqz(bb, fs=fs)  # calculate frequency response
    ...     H_dB= 20 * np.log10(abs(H))  # convert to dB
    ...     ax.plot(f, H_dB, alpha=.5, label=rf"width$={width}\,$Hz")
    ...
    >>> ax.grid()
    >>> ax.legend()
    >>> plt.show()

    It can be seen in the plot above that with increasing width of the transition
    region the suppression in the stopband increases. Since the phase does not vary, it
    is not depicted.

    Instead of defining a transition region width, a window function can also be
    specified. The plot below depicts the response of an 80 tap band-pass filter having
    a passband ranging form 40 Hz to 60 Hz (denoted by a gray background) with
    different windows:

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> import scipy.signal as signal
    ...
    >>> fs, n = 200, 80  # sampling frequency and number of taps
    >>> cutoff = [40, 60]  # corner frequencies (-6 dB gain)
    >>> windows = ('boxcar', 'hamming', 'hann', 'blackman')
    ...
    >>> fg, ax = plt.subplots(1, 1, layout="constrained")  # set up plotting
    >>> ax.set(title=rf"Response of {n}-tap Filter with ${cutoff}\,$Hz passband",
    ...        xlabel=rf"Frequency $f\,$ in hertz (sampling frequency $f_S={fs}\,$Hz)",
    ...        ylabel="Gain in dB", xlim=(0, fs/2))
    >>> ax.axvspan(*cutoff, color='gray', alpha=.25)  # mark passband
    ...
    >>> for win in windows:  # calculate filter and plot response:
    ...     bb = signal.firwin(n, cutoff, window=win, pass_zero=False, fs=fs)
    ...     f, H = signal.freqz(bb, fs=fs)  # calculate frequency response
    ...     H_dB = 20 * np.log10(abs(H))  # convert to dB
    ...     ax.plot(f, H_dB, alpha=.5, label=win)
    ...
    >>> ax.grid()
    >>> ax.legend()
    >>> plt.show()

    The plot shows that the choice of window mainly influences the balance of the
    suppression in the stopband against the width of the transition region. Note that
    utilizing the `~scipy.signal.windows.boxcar` window corresponds to just truncating
    the ideal infinite impulse response to the length of `numtaps` samples.

    The last example illustrates  how to use the `cutoff` and `pass_zero` parameters to
    create a low-pass, a high-pass, a band-stop and a band-pass filter. The desired
    ideal frequency gain is drawn as a gray dashed line whereas the response of the FIR
    filter is depicted as a blue continuous line:

    >>> from itertools import product
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> import scipy.signal as signal
    ...
    >>> cutoffs = [0.5, (.25, .75)]  # cutoff parameters
    >>> fg, axx = plt.subplots(4, 1, sharex='all', layout="constrained",
    ...                        figsize=(5, 4))
    >>> for ax, (cutoff, pass_zero) in zip(axx, product(cutoffs, (True, False))):
    ...     ax.set(title=f"firwin(41, {cutoff=}, {pass_zero=}, fs=2)", ylabel="Gain")
    ...     ax.set_yticks([0.5], minor=True)  # mark gain of 0.5 (= -6 dB)
    ...     ax.grid(which='minor', axis='y')
    ...
    ...     bb = signal.firwin(41, cutoff, pass_zero=pass_zero, fs=2)
    ...     ff, HH = signal.freqz(bb, fs=2)
    ...     ax.plot(ff, abs(HH), 'C0-', label="FIR Response")
    ...
    ...     f_d = np.hstack(([0], np.atleast_1d(cutoff), [1]))
    ...     H_d = np.tile([1, 0] if pass_zero else [0, 1], 2)[:len(f_d)]
    ...     H_d[-1] = H_d[-2] # account for symmetry at Nyquist frequency
    ...     ax.step(f_d, H_d, 'k--', where='post', alpha=.3, label="Desired Response")
    >>> axx[-1].set(xlabel=r"Frequency $f\,$ in hertz (sampling frequency $f_S=2\,$Hz)",
    ...             xlim=(0, 1))
    >>> plt.show()
    """
    # NB: scipy's version of array_namespace returns `np_compat` for int or floats
    xp = array_namespace(cutoff)

    # The major enhancements to this function added in November 2010 were
    # developed by Tom Krauss (see ticket #902).
    fs = _validate_fs(fs, allow_none=True)
    fs = 2 if fs is None else fs

    nyq = 0.5 * fs

    cutoff = xp.asarray(cutoff, dtype=xp_default_dtype(xp))
    cutoff = xpx.atleast_nd(cutoff, ndim=1, xp=xp) / float(nyq)

    # Check for invalid input.
    if cutoff.ndim > 1:
        raise ValueError("The cutoff argument must be at most "
                         "one-dimensional.")
    if xp_size(cutoff) == 0:
        raise ValueError("At least one cutoff frequency must be given.")
    if xp.min(cutoff) <= 0 or xp.max(cutoff) >= 1:
        raise ValueError("Invalid cutoff frequency: frequencies must be "
                         "greater than 0 and less than fs/2.")
    if xp.any(cutoff[1:] - cutoff[:-1] <= 0):
        raise ValueError("Invalid cutoff frequencies: the frequencies "
                         "must be strictly increasing.")

    if width is not None:
        # A width was given.  Find the beta parameter of the Kaiser window
        # and set `window`.  This overrides the value of `window` passed in.
        atten = kaiser_atten(numtaps, float(width) / nyq)
        beta = kaiser_beta(atten)
        window = ('kaiser', beta)

    if pass_zero in ('bandstop', 'lowpass'):
        if pass_zero == 'lowpass':
            if xp_size(cutoff) != 1:
                raise ValueError('cutoff must have one element if '
                                 f'pass_zero=="lowpass", got {cutoff.shape}')
        elif xp_size(cutoff) <= 1:
            raise ValueError('cutoff must have at least two elements if '
                             f'pass_zero=="bandstop", got {cutoff.shape}')
        pass_zero = True
    elif pass_zero in ('bandpass', 'highpass'):
        if pass_zero == 'highpass':
            if xp_size(cutoff) != 1:
                raise ValueError('cutoff must have one element if '
                                 f'pass_zero=="highpass", got {cutoff.shape}')
        elif xp_size(cutoff) <= 1:
            raise ValueError('cutoff must have at least two elements if '
                             f'pass_zero=="bandpass", got {cutoff.shape}')
        pass_zero = False
    elif not (pass_zero is True or pass_zero is False):
        raise ValueError(f"Parameter {pass_zero=} not in (True, False, 'bandpass', " +
                         "'lowpass', 'highpass', 'bandstop')")

    pass_nyquist = (xp_size(cutoff) % 2 == 0) == pass_zero
    if pass_nyquist and numtaps % 2 == 0:
        raise ValueError("A filter with an even number of coefficients must "
                         "have zero response at the Nyquist frequency.")

    # Insert 0 and/or 1 at the ends of cutoff so that the length of cutoff
    # is even, and each pair in cutoff corresponds to passband.
    cutoff = xp.concat((xp.zeros(int(pass_zero)), cutoff, xp.ones(int(pass_nyquist))))


    # `bands` is a 2-D array; each row gives the left and right edges of
    # a passband.
    bands = xp.reshape(cutoff, (-1, 2))

    # Build up the coefficients.
    alpha = 0.5 * (numtaps - 1)
    m = xp.arange(0, numtaps, dtype=cutoff.dtype) - alpha
    h = 0
    for j in range(bands.shape[0]):
        left, right = bands[j, 0], bands[j, 1]
        h += right * xpx.sinc(right * m, xp=xp)
        h -= left * xpx.sinc(left * m, xp=xp)

    # Get and apply the window function.
    win = get_window(window, numtaps, fftbins=False, xp=xp)
    h *= win

    # Now handle scaling if desired.
    if scale:
        # Get the first passband.
        left, right = bands[0, ...]
        if left == 0:
            scale_frequency = 0.0
        elif right == 1:
            scale_frequency = 1.0
        else:
            scale_frequency = 0.5 * (left + right)
        c = xp.cos(xp.pi * m * scale_frequency)
        s = xp.sum(h * c)
        h /= s

    return h

