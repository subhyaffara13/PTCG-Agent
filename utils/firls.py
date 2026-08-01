
def firls(numtaps, bands, desired, *, weight=None, fs=None):
    """
    FIR filter design using least-squares error minimization.

    Calculate the filter coefficients for the linear-phase finite
    impulse response (FIR) filter which has the best approximation
    to the desired frequency response described by `bands` and
    `desired` in the least squares sense (i.e., the integral of the
    weighted mean-squared error within the specified bands is
    minimized).

    Parameters
    ----------
    numtaps : int
        The number of taps in the FIR filter. `numtaps` must be odd.
    bands : array_like
        A monotonic nondecreasing sequence containing the band edges in
        Hz. All elements must be non-negative and less than or equal to
        the Nyquist frequency given by `nyq`. The bands are specified as
        frequency pairs, thus, if using a 1D array, its length must be
        even, e.g., `np.array([0, 1, 2, 3, 4, 5])`. Alternatively, the
        bands can be specified as an nx2 sized 2D array, where n is the
        number of bands, e.g, `np.array([[0, 1], [2, 3], [4, 5]])`.
    desired : array_like
        A sequence the same size as `bands` containing the desired gain
        at the start and end point of each band.
    weight : array_like, optional
        A relative weighting to give to each band region when solving
        the least squares problem. `weight` has to be half the size of
        `bands`.
    fs : float, optional
        The sampling frequency of the signal. Each frequency in `bands`
        must be between 0 and ``fs/2`` (inclusive). Default is 2.

    Returns
    -------
    coeffs : ndarray
        Coefficients of the optimal (in a least squares sense) FIR filter.

    See Also
    --------
    firwin
    firwin2
    minimum_phase
    remez

    Notes
    -----
    This implementation follows the algorithm given in [1]_.
    As noted there, least squares design has multiple advantages:

    1. Optimal in a least-squares sense.
    2. Simple, non-iterative method.
    3. The general solution can obtained by solving a linear
       system of equations.
    4. Allows the use of a frequency dependent weighting function.

    This function constructs a Type I linear phase FIR filter, which
    contains an odd number of `coeffs` satisfying for :math:`n < numtaps`:

    .. math:: coeffs(n) = coeffs(numtaps - 1 - n)

    The odd number of coefficients and filter symmetry avoid boundary
    conditions that could otherwise occur at the Nyquist and 0 frequencies
    (e.g., for Type II, III, or IV variants).

    .. versionadded:: 0.18

    References
    ----------
    .. [1] Ivan Selesnick, Linear-Phase Fir Filter Design By Least Squares.
           OpenStax CNX. Aug 9, 2005.
           https://eeweb.engineering.nyu.edu/iselesni/EL713/firls/firls.pdf

    Examples
    --------
    We want to construct a band-pass filter. Note that the behavior in the
    frequency ranges between our stop bands and pass bands is unspecified,
    and thus may overshoot depending on the parameters of our filter:

    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> fig, axs = plt.subplots(2)
    >>> fs = 10.0  # Hz
    >>> desired = (0, 0, 1, 1, 0, 0)
    >>> for bi, bands in enumerate(((0, 1, 2, 3, 4, 5), (0, 1, 2, 4, 4.5, 5))):
    ...     fir_firls = signal.firls(73, bands, desired, fs=fs)
    ...     fir_remez = signal.remez(73, bands, desired[::2], fs=fs)
    ...     fir_firwin2 = signal.firwin2(73, bands, desired, fs=fs)
    ...     hs = list()
    ...     ax = axs[bi]
    ...     for fir in (fir_firls, fir_remez, fir_firwin2):
    ...         freq, response = signal.freqz(fir)
    ...         hs.append(ax.semilogy(0.5*fs*freq/np.pi, np.abs(response))[0])
    ...     for band, gains in zip(zip(bands[::2], bands[1::2]),
    ...                            zip(desired[::2], desired[1::2])):
    ...         ax.semilogy(band, np.maximum(gains, 1e-7), 'k--', linewidth=2)
    ...     if bi == 0:
    ...         ax.legend(hs, ('firls', 'remez', 'firwin2'),
    ...                   loc='lower center', frameon=False)
    ...     else:
    ...         ax.set_xlabel('Frequency (Hz)')
    ...     ax.grid(True)
    ...     ax.set(title='Band-pass %d-%d Hz' % bands[2:4], ylabel='Magnitude')
    ...
    >>> fig.tight_layout()
    >>> plt.show()

    """
    xp = array_namespace(bands, desired)
    bands = np.asarray(bands)
    desired = np.asarray(desired)

    fs = _validate_fs(fs, allow_none=True)
    fs = 2 if fs is None else fs
    nyq = 0.5 * fs

    numtaps = int(numtaps)
    if numtaps % 2 == 0 or numtaps < 1:
        raise ValueError("numtaps must be odd and >= 1")
    M = (numtaps-1) // 2

    # normalize bands 0->1 and make it 2 columns
    nyq = float(nyq)
    if nyq <= 0:
        raise ValueError(f'nyq must be positive, got {nyq} <= 0.')
    bands = np.asarray(bands).flatten() / nyq
    if len(bands) % 2 != 0:
        raise ValueError("bands must contain frequency pairs.")
    if (bands < 0).any() or (bands > 1).any():
        raise ValueError("bands must be between 0 and 1 relative to Nyquist")
    bands = bands.reshape((-1, 2))

    # check remaining params
    desired = np.asarray(desired).flatten()
    if bands.size != desired.size:
        raise ValueError(
            f"desired must have one entry per frequency, got {desired.size} "
            f"gains for {bands.size} frequencies."
        )
    desired = desired.reshape((-1, 2))
    if (np.diff(bands) <= 0).any() or (np.diff(bands[:, 0]) < 0).any():
        raise ValueError("bands must be monotonically nondecreasing and have "
                         "width > 0.")
    if (bands[:-1, 1] > bands[1:, 0]).any():
        raise ValueError("bands must not overlap.")
    if (desired < 0).any():
        raise ValueError("desired must be non-negative.")
    if weight is None:
        weight = np.ones(len(desired))
    weight = np.asarray(weight).flatten()
    if len(weight) != len(desired):
        raise ValueError("weight must be the same size as the number of "
                         f"band pairs ({len(bands)}).")
    if (weight < 0).any():
        raise ValueError("weight must be non-negative.")

    # Set up the linear matrix equation to be solved, Qa = b

    # We can express Q(k,n) = 0.5 Q1(k,n) + 0.5 Q2(k,n)
    # where Q1(k,n)=q(k-n) and Q2(k,n)=q(k+n), i.e. a Toeplitz plus Hankel.

    # We omit the factor of 0.5 above, instead adding it during coefficient
    # calculation.

    # We also omit the 1/π from both Q and b equations, as they cancel
    # during solving.

    # We have that:
    #     q(n) = 1/π ∫W(ω)cos(nω)dω (over 0->π)
    # Using our normalization ω=πf and with a constant weight W over each
    # interval f1->f2 we get:
    #     q(n) = W∫cos(πnf)df (0->1) = Wf sin(πnf)/πnf
    # integrated over each f1->f2 pair (i.e., value at f2 - value at f1).
    n = np.arange(numtaps)[:, np.newaxis, np.newaxis]
    q = np.dot(np.diff(np.sinc(bands * n) * bands, axis=2)[:, :, 0], weight)

    # Now we assemble our sum of Toeplitz and Hankel
    Q1 = toeplitz(q[:M+1])
    Q2 = hankel(q[:M+1], q[M:])
    Q = Q1 + Q2

    # Now for b(n) we have that:
    #     b(n) = 1/π ∫ W(ω)D(ω)cos(nω)dω (over 0->π)
    # Using our normalization ω=πf and with a constant weight W over each
    # interval and a linear term for D(ω) we get (over each f1->f2 interval):
    #     b(n) = W ∫ (mf+c)cos(πnf)df
    #          = f(mf+c)sin(πnf)/πnf + mf**2 cos(nπf)/(πnf)**2
    # integrated over each f1->f2 pair (i.e., value at f2 - value at f1).
    n = n[:M + 1]  # only need this many coefficients here
    # Choose m and c such that we are at the start and end weights
    m = (np.diff(desired, axis=1) / np.diff(bands, axis=1))
    c = desired[:, [0]] - bands[:, [0]] * m
    b = bands * (m*bands + c) * np.sinc(bands * n)
    # Use L'Hospital's rule here for cos(nπf)/(πnf)**2 @ n=0
    b[0] -= m * bands * bands / 2.
    b[1:] += m * np.cos(n[1:] * np.pi * bands) / (np.pi * n[1:]) ** 2
    b = np.dot(np.diff(b, axis=2)[:, :, 0], weight)

    # Now we can solve the equation
    try:  # try the fast way
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            a = solve(Q, b, assume_a="pos", check_finite=False)
        for ww in w:
            if (ww.category == LinAlgWarning and
                    str(ww.message).startswith('Ill-conditioned matrix')):
                raise LinAlgError(str(ww.message))
    except LinAlgError:  # in case Q is rank deficient
        # This is faster than pinvh, even though we don't explicitly use
        # the symmetry here. gelsy was faster than gelsd and gelss in
        # some non-exhaustive tests.
        a = lstsq(Q, b, lapack_driver='gelsy')[0]

    # make coefficients symmetric (linear phase)
    coeffs = np.hstack((a[:0:-1], 2 * a[0], a[1:]))
    return xp.asarray(coeffs)

