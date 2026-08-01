
def bartlett(M):
    dtype = _dtypes_impl.default_dtypes().float_dtype
    return torch.bartlett_window(M, periodic=False, dtype=dtype)


def bartlett(
    M: int,
    *,
    sym: bool = True,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: torch.device | None = None,
    requires_grad: bool = False,
) -> Tensor:
    if dtype is None:
        dtype = torch.get_default_dtype()

    _window_function_checks("bartlett", M, dtype, layout)

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    if M == 1:
        return torch.ones(
            (1,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    start = -1
    constant = 2 / (M if not sym else M - 1)

    k = torch.linspace(
        start=start,
        end=start + (M - 1) * constant,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    return 1 - torch.abs(k)


def bartlett(*samples, axis=0):
    r"""Perform Bartlett's test for equal variances.

    Bartlett's test tests the null hypothesis that all input samples
    are from populations with equal variances.  For samples
    from significantly non-normal populations, Levene's test
    `levene` is more robust.

    Parameters
    ----------
    *samples : array_like
        arrays of sample data.  Only 1d arrays are accepted, they may have
        different lengths.

    Returns
    -------
    statistic : float
        The test statistic.
    pvalue : float
        The p-value of the test.

    See Also
    --------
    fligner : A non-parametric test for the equality of k variances
    levene : A robust parametric test for equality of k variances
    :ref:`hypothesis_bartlett` : Extended example

    Notes
    -----
    Conover et al. (1981) examine many of the existing parametric and
    nonparametric tests by extensive simulations and they conclude that the
    tests proposed by Fligner and Killeen (1976) and Levene (1960) appear to be
    superior in terms of robustness of departures from normality and power
    ([3]_).

    References
    ----------
    .. [1]  https://www.itl.nist.gov/div898/handbook/eda/section3/eda357.htm
    .. [2]  Snedecor, George W. and Cochran, William G. (1989), Statistical
              Methods, Eighth Edition, Iowa State University Press.
    .. [3] Park, C. and Lindsay, B. G. (1999). Robust Scale Estimation and
           Hypothesis Testing based on Quadratic Inference Function. Technical
           Report #99-03, Center for Likelihood Studies, Pennsylvania State
           University.
    .. [4] Bartlett, M. S. (1937). Properties of Sufficiency and Statistical
           Tests. Proceedings of the Royal Society of London. Series A,
           Mathematical and Physical Sciences, Vol. 160, No.901, pp. 268-282.

    Examples
    --------

    Test whether the lists `a`, `b` and `c` come from populations
    with equal variances.

    >>> import numpy as np
    >>> from scipy import stats
    >>> a = [8.88, 9.12, 9.04, 8.98, 9.00, 9.08, 9.01, 8.85, 9.06, 8.99]
    >>> b = [8.88, 8.95, 9.29, 9.44, 9.15, 9.58, 8.36, 9.18, 8.67, 9.05]
    >>> c = [8.95, 9.12, 8.95, 8.85, 9.03, 8.84, 9.07, 8.98, 8.86, 8.98]
    >>> stat, p = stats.bartlett(a, b, c)
    >>> p
    1.1254782518834628e-05

    The very small p-value suggests that the populations do not have equal
    variances.

    This is not surprising, given that the sample variance of `b` is much
    larger than that of `a` and `c`:

    >>> [np.var(x, ddof=1) for x in [a, b, c]]
    [0.007054444444444413, 0.13073888888888888, 0.008890000000000002]

    For a more detailed example, see :ref:`hypothesis_bartlett`.
    """
    xp = array_namespace(*samples)

    k = len(samples)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")

    if axis is None:
        samples = [xp_ravel(sample) for sample in samples]
    else:
        samples = _broadcast_arrays(samples, axis=axis, xp=xp)
        samples = [xp.moveaxis(sample, axis, -1) for sample in samples]

    Ni = [xp.asarray(_count_nonmasked(sample, axis=-1, xp=xp),
                     dtype=sample.dtype, device=xp_device(sample))
          for sample in samples]
    Ni = [xp.broadcast_to(N, samples[0].shape[:-1]) for N in Ni]
    ssq = [xp.var(sample, correction=1, axis=-1) for sample in samples]
    Ni = [arr[xp.newaxis, ...] for arr in Ni]
    ssq = [arr[xp.newaxis, ...] for arr in ssq]
    Ni = xp.concat(Ni, axis=0)
    Ni = xpx.at(Ni)[Ni == 0].set(xp.nan)
    ssq = xp.concat(ssq, axis=0)
    dtype = Ni.dtype
    Ntot = xp.sum(Ni, axis=0)
    spsq = xp.sum((Ni - 1)*ssq, axis=0, dtype=dtype) / (Ntot - k)
    numer = ((Ntot - k) * xp.log(spsq)
             - xp.sum((Ni - 1)*xp.log(ssq), axis=0, dtype=dtype))
    denom = (1 + 1/(3*(k - 1))
             * ((xp.sum(1/(Ni - 1), axis=0)) - 1/(Ntot - k)))
    T = numer / denom

    chi2 = _SimpleChi2(xp.asarray(k-1, dtype=dtype, device=xp_device(T)))
    pvalue = _get_pvalue(T, chi2, alternative='greater', symmetric=False, xp=xp)

    T = xp.clip(T, min=0., max=xp.inf)
    T = T[()] if T.ndim == 0 else T
    pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue

    return BartlettResult(T, pvalue)


def bartlett(M, sym=True, *, xp=None, device=None):
    r"""
    Return a Bartlett window.

    The Bartlett window is very similar to a triangular window, except
    that the end points are at zero.  It is often used in signal
    processing for tapering a signal, without generating too much
    ripple in the frequency domain.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero, an empty array
        is returned. An exception is thrown when it is negative.
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter
        design.
        When False, generates a periodic window, for use in spectral analysis.
    %(xp_device_snippet)s

    Returns
    -------
    w : ndarray
        The triangular window, with the first and last samples equal to zero
        and the maximum value normalized to 1 (though the value 1 does not
        appear if `M` is even and `sym` is True).

    See Also
    --------
    triang : A triangular window that does not touch zero at the ends

    Notes
    -----
    The Bartlett window is defined as

    .. math:: w(n) = \frac{2}{M-1} \left(
              \frac{M-1}{2} - \left|n - \frac{M-1}{2}\right|
              \right)

    Most references to the Bartlett window come from the signal
    processing literature, where it is used as one of many windowing
    functions for smoothing values.  Note that convolution with this
    window produces linear interpolation.  It is also known as an
    apodization (which means"removing the foot", i.e. smoothing
    discontinuities at the beginning and end of the sampled signal) or
    tapering function. The Fourier transform of the Bartlett is the product
    of two sinc functions.
    Note the excellent discussion in Kanasewich. [2]_

    References
    ----------
    .. [1] M.S. Bartlett, "Periodogram Analysis and Continuous Spectra",
           Biometrika 37, 1-16, 1950.
    .. [2] E.R. Kanasewich, "Time Sequence Analysis in Geophysics",
           The University of Alberta Press, 1975, pp. 109-110.
    .. [3] A.V. Oppenheim and R.W. Schafer, "Discrete-Time Signal
           Processing", Prentice-Hall, 1999, pp. 468-471.
    .. [4] Wikipedia, "Window function",
           https://en.wikipedia.org/wiki/Window_function
    .. [5] W.H. Press,  B.P. Flannery, S.A. Teukolsky, and W.T. Vetterling,
           "Numerical Recipes", Cambridge University Press, 1986, page 429.

    Examples
    --------
    Plot the window and its frequency response:

    >>> import numpy as np
    >>> from scipy import signal
    >>> from scipy.fft import fft, fftshift
    >>> import matplotlib.pyplot as plt

    >>> window = signal.windows.bartlett(51)
    >>> plt.plot(window)
    >>> plt.title("Bartlett window")
    >>> plt.ylabel("Amplitude")
    >>> plt.xlabel("Sample")

    >>> plt.figure()
    >>> A = fft(window, 2048) / (len(window)/2.0)
    >>> freq = np.linspace(-0.5, 0.5, len(A))
    >>> response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
    >>> plt.plot(freq, response)
    >>> plt.axis([-0.5, 0.5, -120, 0])
    >>> plt.title("Frequency response of the Bartlett window")
    >>> plt.ylabel("Normalized magnitude [dB]")
    >>> plt.xlabel("Normalized frequency [cycles per sample]")

    """
    # Docstring adapted from NumPy's bartlett function
    xp = _namespace(xp)

    if _len_guards(M):
        return xp.ones(M, dtype=xp.float64, device=device)
    M, needs_trunc = _extend(M, sym)

    n = xp.arange(0, M, dtype=xp.float64, device=device)

    # cf https://github.com/data-apis/array-api-strict/issues/77
    w = xp.where(n <= (M - 1) / 2.0,
                 2.0 * n / (M - 1), 2.0 - 2.0 * n / (M - 1))

    return _truncate(w, needs_trunc)


def bartlett(M):
    """
    Return the Bartlett window.

    The Bartlett window is very similar to a triangular window, except
    that the end points are at zero.  It is often used in signal
    processing for tapering a signal, without generating too much
    ripple in the frequency domain.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero or less, an
        empty array is returned.

    Returns
    -------
    out : array
        The triangular window, with the maximum value normalized to one
        (the value one appears only if the number of samples is odd), with
        the first and last samples equal to zero.

    See Also
    --------
    blackman, hamming, hanning, kaiser

    Notes
    -----
    The Bartlett window is defined as

    .. math:: w(n) = \\frac{2}{M-1} \\left(
              \\frac{M-1}{2} - \\left|n - \\frac{M-1}{2}\\right|
              \\right)

    Most references to the Bartlett window come from the signal processing
    literature, where it is used as one of many windowing functions for
    smoothing values.  Note that convolution with this window produces linear
    interpolation.  It is also known as an apodization (which means "removing
    the foot", i.e. smoothing discontinuities at the beginning and end of the
    sampled signal) or tapering function. The Fourier transform of the
    Bartlett window is the product of two sinc functions. Note the excellent
    discussion in Kanasewich [2]_.

    References
    ----------
    .. [1] M.S. Bartlett, "Periodogram Analysis and Continuous Spectra",
           Biometrika 37, 1-16, 1950.
    .. [2] E.R. Kanasewich, "Time Sequence Analysis in Geophysics",
           The University of Alberta Press, 1975, pp. 109-110.
    .. [3] A.V. Oppenheim and R.W. Schafer, "Discrete-Time Signal
           Processing", Prentice-Hall, 1999, pp. 468-471.
    .. [4] Wikipedia, "Window function",
           https://en.wikipedia.org/wiki/Window_function
    .. [5] W.H. Press,  B.P. Flannery, S.A. Teukolsky, and W.T. Vetterling,
           "Numerical Recipes", Cambridge University Press, 1986, page 429.

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> np.bartlett(12)
    array([ 0.        ,  0.18181818,  0.36363636,  0.54545455,  0.72727273, # may vary
            0.90909091,  0.90909091,  0.72727273,  0.54545455,  0.36363636,
            0.18181818,  0.        ])

    Plot the window and its frequency response (requires SciPy and matplotlib).

    .. plot::
        :include-source:

        import matplotlib.pyplot as plt
        from numpy.fft import fft, fftshift
        window = np.bartlett(51)
        plt.plot(window)
        plt.title("Bartlett window")
        plt.ylabel("Amplitude")
        plt.xlabel("Sample")
        plt.show()
        plt.figure()
        A = fft(window, 2048) / 25.5
        mag = np.abs(fftshift(A))
        freq = np.linspace(-0.5, 0.5, len(A))
        with np.errstate(divide='ignore', invalid='ignore'):
            response = 20 * np.log10(mag)
        response = np.clip(response, -100, 100)
        plt.plot(freq, response)
        plt.title("Frequency response of Bartlett window")
        plt.ylabel("Magnitude [dB]")
        plt.xlabel("Normalized frequency [cycles per sample]")
        plt.axis('tight')
        plt.show()

    """
    # Ensures at least float64 via 0.0.  M should be an integer, but conversion
    # to double is safe for a range.
    values = np.array([0.0, M])
    M = values[1]

    if M < 1:
        return array([], dtype=values.dtype)
    if M == 1:
        return ones(1, dtype=values.dtype)
    n = arange(1 - M, M, 2)
    return where(less_equal(n, 0), 1 + n / (M - 1), 1 - n / (M - 1))


def bartlett(M: int) -> Array:
  """Return a Bartlett window of size M.

  JAX implementation of :func:`numpy.bartlett`.

  Args:
    M: The window size.

  Returns:
    An array of size M containing the Bartlett window.

  Examples:
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.bartlett(4))
    [0.   0.67 0.67 0.  ]

  See also:
    - :func:`jax.numpy.blackman`: return a Blackman window of size M.
    - :func:`jax.numpy.hamming`: return a Hamming window of size M.
    - :func:`jax.numpy.hanning`: return a Hanning window of size M.
    - :func:`jax.numpy.kaiser`: return a Kaiser window of size M.
  """
  M = core.concrete_or_error(int, M, "M argument of jnp.bartlett")
  dtype = dtypes.default_float_dtype()
  if M <= 1:
    return lax.full((M,), 1, dtype)
  n = lax.iota(dtype, M)
  return 1 - ufuncs.abs(2 * n + 1 - M) / (M - 1)

