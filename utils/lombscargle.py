
def lombscargle(
    x: npt.ArrayLike,
    y: npt.ArrayLike,
    freqs: npt.ArrayLike,
    *,
    precenter: bool = _NoValue,  # type:ignore[assignment]
    normalize: bool | Literal["power", "normalize", "amplitude"] = False,
    weights: npt.NDArray | None = None,
    floating_mean: bool = False,
) -> npt.NDArray:
    """
    Compute the generalized Lomb-Scargle periodogram.

    The Lomb-Scargle periodogram was developed by Lomb [1]_ and further
    extended by Scargle [2]_ to find, and test the significance of weak
    periodic signals with uneven temporal sampling. The algorithm used
    here is based on a weighted least-squares fit of the form
    ``y(ω) = a*cos(ω*x) + b*sin(ω*x) + c``, where the fit is calculated for
    each frequency independently. This algorithm was developed by Zechmeister
    and Kürster which improves the Lomb-Scargle periodogram by enabling
    the weighting of individual samples and calculating an unknown y offset
    (also called a "floating-mean" model) [3]_. For more details, and practical
    considerations, see the excellent reference on the Lomb-Scargle periodogram [4]_.

    When *normalize* is False (or "power") (default) the computed periodogram
    is unnormalized, it takes the value ``(A**2) * N/4`` for a harmonic
    signal with amplitude A for sufficiently large N. Where N is the length of x or y.

    When *normalize* is True (or "normalize") the computed periodogram is normalized
    by the residuals of the data around a constant reference model (at zero).

    When *normalize* is "amplitude" the computed periodogram is the complex
    representation of the amplitude and phase.

    Input arrays should be 1-D of a real floating data type, which are converted into
    float64 arrays before processing.

    Parameters
    ----------
    x : array_like
        Sample times.
    y : array_like
        Measurement values. Values are assumed to have a baseline of ``y = 0``. If
        there is a possibility of a y offset, it is recommended to set `floating_mean`
        to True.
    freqs : array_like
        Angular frequencies (e.g., having unit rad/s=2π/s for `x` having unit s) for
        output periodogram. Frequencies are normally >= 0, as any peak at ``-freq`` will
        also exist at ``+freq``.
    precenter : bool, optional
        Pre-center measurement values by subtracting the mean, if True. This is
        a legacy parameter and unnecessary if `floating_mean` is True.

        .. deprecated:: 1.17.0
            The `precenter` argument is deprecated and will be removed in SciPy 1.19.0.
            The functionality can be substituted by passing ``y - y.mean()`` to `y`.

    normalize : bool | str, optional
        Compute normalized or complex (amplitude + phase) periodogram.
        Valid options are: ``False``/``"power"``, ``True``/``"normalize"``, or
        ``"amplitude"``.
    weights : array_like, optional
        Weights for each sample. Weights must be nonnegative.
    floating_mean : bool, optional
        Determines a y offset for each frequency independently, if True.
        Else the y offset is assumed to be `0`.

    Returns
    -------
    pgram : array_like
        Lomb-Scargle periodogram.

    Raises
    ------
    ValueError
        If any of the input arrays x, y, freqs, or weights are not 1D, or if any are
        zero length. Or, if the input arrays x, y, and weights do not have the same
        shape as each other.
    ValueError
        If any weight is < 0, or the sum of the weights is <= 0.
    ValueError
        If the normalize parameter is not one of the allowed options.

    See Also
    --------
    periodogram: Power spectral density using a periodogram
    welch: Power spectral density by Welch's method
    csd: Cross spectral density by Welch's method

    Notes
    -----
    The algorithm used will not automatically account for any unknown y offset, unless
    `floating_mean` is ``True``. Therefore, for most use cases, if there is a
    possibility of a y offset, it is recommended to set `floating_mean` to ``True``.
    Furthermore, `floating_mean` accounts for sample weights, and will also correct for
    any bias due to consistently missing observations at peaks and/or troughs.

    The legacy concept of "pre-centering" entails removing the mean from parameter `y`
    before processing, i.e., passing ``y - y.mean()`` instead of setting the parameter
    `floating_mean` to ``True``.

    When the normalize parameter is "amplitude", for any frequency in freqs that is
    below ``(2*pi)/(x.max() - x.min())``, the predicted amplitude will tend towards
    infinity. The concept of a "Nyquist frequency" limit (see Nyquist-Shannon sampling
    theorem) is not generally applicable to unevenly sampled data. Therefore, with
    unevenly sampled data, valid frequencies in freqs can often be much higher than
    expected for those familiar with methods like FFT.

    References
    ----------
    .. [1] N.R. Lomb "Least-squares frequency analysis of unequally spaced
           data", Astrophysics and Space Science, vol 39, pp. 447-462, 1976
           :doi:`10.1007/bf00648343`

    .. [2] J.D. Scargle "Studies in astronomical time series analysis. II -
           Statistical aspects of spectral analysis of unevenly spaced data",
           The Astrophysical Journal, vol 263, pp. 835-853, 1982
           :doi:`10.1086/160554`

    .. [3] M. Zechmeister and M. Kürster, "The generalised Lomb-Scargle periodogram.
           A new formalism for the floating-mean and Keplerian periodograms,"
           Astronomy and Astrophysics, vol. 496, pp. 577-584, 2009
           :doi:`10.1051/0004-6361:200811296`

    .. [4] J.T. VanderPlas, "Understanding the Lomb-Scargle Periodogram,"
           The Astrophysical Journal Supplement Series, vol. 236, no. 1, p. 16,
           May 2018
           :doi:`10.3847/1538-4365/aab766`


    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng()

    First define some input parameters for the signal:

    >>> A = 2.  # amplitude
    >>> c = 2.  # offset
    >>> w0 = 1.  # rad/sec
    >>> nin = 150
    >>> nout = 1002

    Randomly generate sample times:

    >>> x = rng.uniform(0, 10*np.pi, nin)

    Plot a sine wave for the selected times:

    >>> y = A * np.cos(w0*x) + c

    Define the array of frequencies for which to compute the periodogram:

    >>> w = np.linspace(0.25, 10, nout)

    Calculate Lomb-Scargle periodogram for each of the normalize options:

    >>> from scipy.signal import lombscargle
    >>> pgram_power = lombscargle(x, y, w, normalize=False)
    >>> pgram_norm = lombscargle(x, y, w, normalize=True)
    >>> pgram_amp = lombscargle(x, y, w, normalize='amplitude')
    ...
    >>> pgram_power_f = lombscargle(x, y, w, normalize=False, floating_mean=True)
    >>> pgram_norm_f = lombscargle(x, y, w, normalize=True, floating_mean=True)
    >>> pgram_amp_f = lombscargle(x, y, w, normalize='amplitude', floating_mean=True)

    Now make a plot of the input data:

    >>> import matplotlib.pyplot as plt
    >>> fig, (ax_t, ax_p, ax_n, ax_a) = plt.subplots(4, 1, figsize=(5, 6))
    >>> ax_t.plot(x, y, 'b+')
    >>> ax_t.set_xlabel('Time [s]')
    >>> ax_t.set_ylabel('Amplitude')

    Then plot the periodogram for each of the normalize options, as well as with and
    without floating_mean=True:

    >>> ax_p.plot(w, pgram_power, label='default')
    >>> ax_p.plot(w, pgram_power_f, label='floating_mean=True')
    >>> ax_p.set_xlabel('Angular frequency [rad/s]')
    >>> ax_p.set_ylabel('Power')
    >>> ax_p.legend(prop={'size': 7})
    ...
    >>> ax_n.plot(w, pgram_norm, label='default')
    >>> ax_n.plot(w, pgram_norm_f, label='floating_mean=True')
    >>> ax_n.set_xlabel('Angular frequency [rad/s]')
    >>> ax_n.set_ylabel('Normalized')
    >>> ax_n.legend(prop={'size': 7})
    ...
    >>> ax_a.plot(w, np.abs(pgram_amp), label='default')
    >>> ax_a.plot(w, np.abs(pgram_amp_f), label='floating_mean=True')
    >>> ax_a.set_xlabel('Angular frequency [rad/s]')
    >>> ax_a.set_ylabel('Amplitude')
    >>> ax_a.legend(prop={'size': 7})
    ...
    >>> plt.tight_layout()
    >>> plt.show()

    """

    # if no weights are provided, assume all data points are equally important
    if weights is None:
        weights = np.ones_like(y, dtype=np.float64)
    else:
        # if provided, make sure weights is an array and cast to float64
        weights = np.asarray(weights, dtype=np.float64)

    # make sure other inputs are arrays and cast to float64
    # done before validation, in case they were not arrays
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    freqs = np.asarray(freqs, dtype=np.float64)

    # validate input shapes
    if not (x.ndim == 1 and x.size > 0 and x.shape == y.shape == weights.shape):
        raise ValueError("Parameters x, y, weights must be 1-D arrays of "
                         "equal non-zero length!")
    if not (freqs.ndim == 1 and freqs.size > 0):
        raise ValueError("Parameter freqs must be a 1-D array of non-zero length!")

    # validate weights
    if not (np.all(weights >= 0) and np.sum(weights) > 0):
        raise ValueError("Parameter weights must have only non-negative entries "
                         "which sum to a positive value!")

    # validate normalize parameter
    if isinstance(normalize, bool):
        # if bool, convert to str literal
        normalize = "normalize" if normalize else "power"

    if normalize not in ["power", "normalize", "amplitude"]:
        raise ValueError(
            "Normalize must be: False (or 'power'), True (or 'normalize'), "
            "or 'amplitude'."
        )

    # weight vector must sum to 1
    weights = weights * (1.0 / weights.sum())

    # if requested, perform precenter
    if precenter is not _NoValue:
        msg = ("Use of parameter 'precenter' is deprecated as of SciPy 1.17.0 and "
               "will be removed in 1.19.0. Please leave 'precenter' unspecified. "
               "Passing True to 'precenter' "
               "can be exactly substituted by passing 'y = (y - y.mean())' into "
               "the input. Consider setting `floating_mean` to True instead.")
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        if precenter:
            y = y - y.mean()

    # transform arrays
    # row vector
    freqs = freqs.reshape(1, -1)
    # column vectors
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)  # type:ignore[union-attr]
    weights = weights.reshape(-1, 1)

    # store frequent intermediates
    weights_y = weights * y
    freqst = freqs * x
    coswt = np.cos(freqst)
    sinwt = np.sin(freqst)

    Y = np.dot(weights.T, y)  # Eq. 7
    CC = np.dot(weights.T, coswt * coswt)  # Eq. 13
    SS = 1.0 - CC  # trig identity: S^2 = 1 - C^2  Eq.14
    CS = np.dot(weights.T, coswt * sinwt)  # Eq. 15

    if floating_mean:
        C = np.dot(weights.T, coswt)  # Eq. 8
        S = np.dot(weights.T, sinwt)  # Eq. 9
        CC -= C * C  # Eq. 13
        SS -= S * S  # Eq. 14
        CS -= C * S  # Eq. 15

    # calculate tau (phase offset to eliminate CS variable)
    tau = 0.5 * np.arctan2(2.0 * CS, CC - SS)  # Eq. 19
    freqst_tau = freqst - tau

    # coswt and sinwt are now offset by tau, which eliminates CS
    coswt_tau = np.cos(freqst_tau)
    sinwt_tau = np.sin(freqst_tau)

    YC = np.dot(weights_y.T, coswt_tau)  # Eq. 11
    YS = np.dot(weights_y.T, sinwt_tau)  # Eq. 12
    CC = np.dot(weights.T, coswt_tau * coswt_tau)  # Eq. 13, CC range is [0.5, 1.0]
    SS = 1.0 - CC  # trig identity: S^2 = 1 - C^2    Eq. 14, SS range is [0.0, 0.5]

    if floating_mean:
        C = np.dot(weights.T, coswt_tau)  # Eq. 8
        S = np.dot(weights.T, sinwt_tau)  # Eq. 9
        YC -= Y * C  # Eq. 11
        YS -= Y * S  # Eq. 12
        CC -= C * C  # Eq. 13, CC range is now [0.0, 1.0]
        SS -= S * S  # Eq. 14, SS range is now [0.0, 0.5]

    # to prevent division by zero errors with a and b, as well as correcting for
    # numerical precision errors that lead to CC or SS being approximately -0.0,
    # make sure CC and SS are both > 0
    epsneg = np.finfo(dtype=y.dtype).epsneg  # type:ignore[union-attr]
    CC[CC < epsneg] = epsneg
    SS[SS < epsneg] = epsneg

    # calculate a and b
    # where: y(w) = a*cos(w) + b*sin(w) + c
    a = YC / CC  # Eq. A.4 and 6, eliminating CS
    b = YS / SS  # Eq. A.4 and 6, eliminating CS
    # c = Y - a * C - b * S

    # store final value as power in A^2 (i.e., (y units)^2)
    pgram = 2.0 * (a * YC + b * YS)

    # squeeze back to a vector
    pgram = np.squeeze(pgram)

    if normalize == "power":  # (default)
        # return the legacy power units ((A**2) * N/4)

        pgram *= float(x.shape[0]) / 4.0

    elif normalize == "normalize":
        # return the normalized power (power at current frequency wrt the entire signal)
        # range will be [0, 1]

        YY = np.dot(weights_y.T, y)  # Eq. 10
        if floating_mean:
            YY -= Y * Y  # Eq. 10

        pgram *= 0.5 / np.squeeze(YY)  # Eq. 20

    else:  # normalize == "amplitude":
        # return the complex representation of the best-fit amplitude and phase

        # squeeze back to vectors
        a = np.squeeze(a)
        b = np.squeeze(b)
        tau = np.squeeze(tau)

        # calculate the complex representation, and correct for tau rotation
        pgram = (a + 1j * b) * np.exp(1j * tau)

    return pgram

