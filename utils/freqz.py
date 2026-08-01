
def freqz(b, a=1, worN=512, whole=False, plot=None, fs=2*pi,
          include_nyquist=False):
    """
    Compute the frequency response of a digital filter.

    Given the M-order numerator `b` and N-order denominator `a` of a digital
    filter, compute its frequency response::

                 jw                 -jw              -jwM
        jw    B(e  )    b[0] + b[1]e    + ... + b[M]e
     H(e  ) = ------ = -----------------------------------
                 jw                 -jw              -jwN
              A(e  )    a[0] + a[1]e    + ... + a[N]e

    Parameters
    ----------
    b : array_like
        Numerator of a linear filter. If `b` has dimension greater than 1,
        it is assumed that the coefficients are stored in the first dimension,
        and ``b.shape[1:]``, ``a.shape[1:]``, and the shape of the frequencies
        array must be compatible for broadcasting.
    a : array_like
        Denominator of a linear filter. If `b` has dimension greater than 1,
        it is assumed that the coefficients are stored in the first dimension,
        and ``b.shape[1:]``, ``a.shape[1:]``, and the shape of the frequencies
        array must be compatible for broadcasting.
    worN : {None, int, array_like}, optional
        If a single integer, then compute at that many frequencies (default is
        N=512). This is a convenient alternative to::

            np.linspace(0, fs if whole else fs/2, N, endpoint=include_nyquist)

        Using a number that is fast for FFT computations can result in
        faster computations (see Notes).

        If an array_like, compute the response at the frequencies given.
        These are in the same units as `fs`.
    whole : bool, optional
        Normally, frequencies are computed from 0 to the Nyquist frequency,
        fs/2 (upper-half of unit-circle). If `whole` is True, compute
        frequencies from 0 to fs. Ignored if worN is array_like.
    plot : callable
        A callable that takes two arguments. If given, the return parameters
        `w` and `h` are passed to plot. Useful for plotting the frequency
        response inside `freqz`.
    fs : float, optional
        The sampling frequency of the digital system. Defaults to 2*pi
        radians/sample (so w is from 0 to pi).

        .. versionadded:: 1.2.0
    include_nyquist : bool, optional
        If `whole` is False and `worN` is an integer, setting `include_nyquist`
        to True will include the last frequency (Nyquist frequency) and is
        otherwise ignored.

        .. versionadded:: 1.5.0

    Returns
    -------
    w : ndarray
        The frequencies at which `h` was computed, in the same units as `fs`.
        By default, `w` is normalized to the range [0, pi) (radians/sample).
    h : ndarray
        The frequency response, as complex numbers.

    See Also
    --------
    freqz_zpk
    freqz_sos

    Notes
    -----
    Using Matplotlib's :func:`matplotlib.pyplot.plot` function as the callable
    for `plot` produces unexpected results, as this plots the real part of the
    complex transfer function, not the magnitude.
    Try ``lambda w, h: plot(w, np.abs(h))``.

    A direct computation via (R)FFT is used to compute the frequency response
    when the following conditions are met:

    1. An integer value is given for `worN`.
    2. `worN` is fast to compute via FFT (i.e.,
       `next_fast_len(worN) <scipy.fft.next_fast_len>` equals `worN`).
    3. The denominator coefficients are a single value (``a.shape[0] == 1``).
    4. `worN` is at least as long as the numerator coefficients
       (``worN >= b.shape[0]``).
    5. If ``b.ndim > 1``, then ``b.shape[-1] == 1``.

    For long FIR filters, the FFT approach can have lower error and be much
    faster than the equivalent direct polynomial calculation.

    Examples
    --------
    >>> from scipy import signal
    >>> import numpy as np
    >>> taps, f_c = 80, 1.0  # number of taps and cut-off frequency
    >>> b = signal.firwin(taps, f_c, window=('kaiser', 8), fs=2*np.pi)
    >>> w, h = signal.freqz(b)

    >>> import matplotlib.pyplot as plt
    >>> fig, ax1 = plt.subplots(tight_layout=True)
    >>> ax1.set_title(f"Frequency Response of {taps} tap FIR Filter" +
    ...               f"($f_c={f_c}$ rad/sample)")
    >>> ax1.axvline(f_c, color='black', linestyle=':', linewidth=0.8)
    >>> ax1.plot(w, 20 * np.log10(abs(h)), 'C0')
    >>> ax1.set_ylabel("Amplitude in dB", color='C0')
    >>> ax1.set(xlabel="Frequency in rad/sample", xlim=(0, np.pi))

    >>> ax2 = ax1.twinx()
    >>> phase = np.unwrap(np.angle(h))
    >>> ax2.plot(w, phase, 'C1')
    >>> ax2.set_ylabel('Phase [rad]', color='C1')
    >>> ax2.grid(True)
    >>> ax2.axis('tight')
    >>> plt.show()

    Broadcasting Examples

    Suppose we have two FIR filters whose coefficients are stored in the
    rows of an array with shape (2, 25). For this demonstration, we'll
    use random data:

    >>> rng = np.random.default_rng()
    >>> b = rng.random((2, 25))

    To compute the frequency response for these two filters with one call
    to `freqz`, we must pass in ``b.T``, because `freqz` expects the first
    axis to hold the coefficients. We must then extend the shape with a
    trivial dimension of length 1 to allow broadcasting with the array
    of frequencies.  That is, we pass in ``b.T[..., np.newaxis]``, which has
    shape (25, 2, 1):

    >>> w, h = signal.freqz(b.T[..., np.newaxis], worN=1024)
    >>> w.shape
    (1024,)
    >>> h.shape
    (2, 1024)

    Now, suppose we have two transfer functions, with the same numerator
    coefficients ``b = [0.5, 0.5]``. The coefficients for the two denominators
    are stored in the first dimension of the 2-D array  `a`::

        a = [   1      1  ]
            [ -0.25, -0.5 ]

    >>> b = np.array([0.5, 0.5])
    >>> a = np.array([[1, 1], [-0.25, -0.5]])

    Only `a` is more than 1-D. To make it compatible for
    broadcasting with the frequencies, we extend it with a trivial dimension
    in the call to `freqz`:

    >>> w, h = signal.freqz(b, a[..., np.newaxis], worN=1024)
    >>> w.shape
    (1024,)
    >>> h.shape
    (2, 1024)

    """
    xp = array_namespace(b, a)

    b, a = map(xp.asarray, (b, a))
    if xp.isdtype(a.dtype, 'integral'):
        a = xp.astype(a, xp_default_dtype(xp))
    res_dtype = xp.result_type(b, a)
    real_dtype = _real_dtype_for_complex(res_dtype, xp=xp)

    b = xpx.atleast_nd(b, ndim=1, xp=xp)
    a = xpx.atleast_nd(a, ndim=1, xp=xp)

    fs = _validate_fs(fs, allow_none=False)

    if worN is None:
        # For backwards compatibility
        worN = 512

    h = None

    if _is_int_type(worN):
        N = operator.index(worN)
        del worN
        if N < 0:
            raise ValueError(f'worN must be nonnegative, got {N}')
        lastpoint = 2 * pi if whole else pi
        # if include_nyquist is true and whole is false, w should
        # include end point
        w = xp.linspace(0, lastpoint, N,
                        endpoint=include_nyquist and not whole, dtype=real_dtype)
        n_fft = N if whole else 2 * (N - 1) if include_nyquist else 2 * N
        if (xp_size(a) == 1 and (b.ndim == 1 or (b.shape[-1] == 1))
                and n_fft >= b.shape[0]
                and n_fft > 0):  # TODO: review threshold acc. to benchmark?

            if (xp.isdtype(b.dtype, "real floating") and
                xp.isdtype(a.dtype, "real floating")
            ):
                fft_func = sp_fft.rfft
            else:
                fft_func = sp_fft.fft

            h = fft_func(b, n=n_fft, axis=0)
            h = h[:min(N, h.shape[0]), ...]
            h /= a

            if fft_func is sp_fft.rfft and whole:
                # exclude DC and maybe Nyquist (no need to use axis_reverse
                # here because we can build reversal with the truncation)
                stop = None if n_fft % 2 == 1 else -1
                h_flipped = xp.flip(h[1:stop, ...], axis=0)
                h = xp.concat((h, xp.conj(h_flipped)))
            if b.ndim > 1:
                # Last axis of h has length 1, so drop it.
                h = h[..., 0]
                # Move the first axis of h to the end.
                h = xp.moveaxis(h, 0, -1)
    else:
        if isinstance(worN, complex):
            # backwards compat
            worN = worN.real
        w = xpx.atleast_nd(xp.asarray(worN, dtype=res_dtype), ndim=1, xp=xp)
        if xp.isdtype(w.dtype, 'integral'):
            w = xp.astype(w, xp_default_dtype(xp))
        del worN
        w = 2 * pi * w / fs

    if h is None:  # still need to compute using freqs w
        zm1 = xp.exp(-1j * w)
        h = (_pu.npp_polyval(zm1, b, tensor=False, xp=xp) /
             _pu.npp_polyval(zm1, a, tensor=False, xp=xp))

    w = w * (fs / (2 * pi))

    if plot is not None:
        plot(w, h)

    return w, h

