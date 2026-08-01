
def kaiser(M, beta):
    dtype = _dtypes_impl.default_dtypes().float_dtype
    return torch.kaiser_window(M, beta=beta, periodic=False, dtype=dtype)


def kaiser(
    M: int,
    *,
    beta: float = 12.0,
    sym: bool = True,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: torch.device | None = None,
    requires_grad: bool = False,
) -> Tensor:
    if dtype is None:
        dtype = torch.get_default_dtype()

    _window_function_checks("kaiser", M, dtype, layout)

    if beta < 0:
        raise ValueError(f"beta must be non-negative, got: {beta} instead.")

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    if M == 1:
        return torch.ones(
            (1,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    # Avoid NaNs by casting `beta` to the appropriate dtype.
    # pyrefly: ignore [bad-assignment]
    beta = torch.tensor(beta, dtype=dtype, device=device)

    start = -beta
    constant = 2.0 * beta / (M if not sym else M - 1)
    end = torch.minimum(
        # pyrefly: ignore [bad-argument-type]
        beta,
        # pyrefly: ignore [bad-argument-type]
        start + (M - 1) * constant,
    )

    k = torch.linspace(
        start=start,
        end=end,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    return torch.i0(torch.sqrt(beta * beta - torch.pow(k, 2))) / torch.i0(
        # pyrefly: ignore [bad-argument-type]
        beta
    )


def kaiser(M, beta, sym=True, *, xp=None, device=None):
    r"""Return a Kaiser window.

    The Kaiser window is a taper formed by using a Bessel function.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero, an empty array
        is returned. An exception is thrown when it is negative.
    beta : float
        Shape parameter, determines trade-off between main-lobe width and
        side lobe level. As beta gets large, the window narrows.
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter
        design.
        When False, generates a periodic window, for use in spectral analysis.
    %(xp_device_snippet)s

    Returns
    -------
    w : ndarray
        The window, with the maximum value normalized to 1 (though the value 1
        does not appear if `M` is even and `sym` is True).

    Notes
    -----
    The Kaiser window is defined as

    .. math::  w(n) = I_0\left( \beta \sqrt{1-\frac{4n^2}{(M-1)^2}}
               \right)/I_0(\beta)

    with

    .. math:: \quad -\frac{M-1}{2} \leq n \leq \frac{M-1}{2},

    where :math:`I_0` is the modified zeroth-order Bessel function.

    The Kaiser was named for Jim Kaiser, who discovered a simple approximation
    to the DPSS window based on Bessel functions.
    The Kaiser window is a very good approximation to the discrete prolate
    spheroidal sequence, or Slepian window, which is the transform which
    maximizes the energy in the main lobe of the window relative to total
    energy.

    The Kaiser can approximate other windows by varying the beta parameter.
    (Some literature uses alpha = beta/pi.) [4]_

    ====  =======================
    beta  Window shape
    ====  =======================
    0     Rectangular
    5     Similar to a Hamming
    6     Similar to a Hann
    8.6   Similar to a Blackman
    ====  =======================

    A beta value of 14 is probably a good starting point. Note that as beta
    gets large, the window narrows, and so the number of samples needs to be
    large enough to sample the increasingly narrow spike, otherwise NaNs will
    be returned.

    Most references to the Kaiser window come from the signal processing
    literature, where it is used as one of many windowing functions for
    smoothing values.  It is also known as an apodization (which means
    "removing the foot", i.e. smoothing discontinuities at the beginning
    and end of the sampled signal) or tapering function.

    References
    ----------
    .. [1] J. F. Kaiser, "Digital Filters" - Ch 7 in "Systems analysis by
           digital computer", Editors: F.F. Kuo and J.F. Kaiser, p 218-285.
           John Wiley and Sons, New York, (1966).
    .. [2] E.R. Kanasewich, "Time Sequence Analysis in Geophysics", The
           University of Alberta Press, 1975, pp. 177-178.
    .. [3] Wikipedia, "Window function",
           https://en.wikipedia.org/wiki/Window_function
    .. [4] F. J. Harris, "On the use of windows for harmonic analysis with the
           discrete Fourier transform," Proceedings of the IEEE, vol. 66,
           no. 1, pp. 51-83, Jan. 1978. :doi:`10.1109/PROC.1978.10837`.

    Examples
    --------
    Plot the window and its frequency response:

    >>> import numpy as np
    >>> from scipy import signal
    >>> from scipy.fft import fft, fftshift
    >>> import matplotlib.pyplot as plt

    >>> window = signal.windows.kaiser(51, beta=14)
    >>> plt.plot(window)
    >>> plt.title(r"Kaiser window ($\beta$=14)")
    >>> plt.ylabel("Amplitude")
    >>> plt.xlabel("Sample")

    >>> plt.figure()
    >>> A = fft(window, 2048) / (len(window)/2.0)
    >>> freq = np.linspace(-0.5, 0.5, len(A))
    >>> response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
    >>> plt.plot(freq, response)
    >>> plt.axis([-0.5, 0.5, -120, 0])
    >>> plt.title(r"Frequency response of the Kaiser window ($\beta$=14)")
    >>> plt.ylabel("Normalized magnitude [dB]")
    >>> plt.xlabel("Normalized frequency [cycles per sample]")

    """
    xp = _namespace(xp)

    # Docstring adapted from NumPy's kaiser function
    if _len_guards(M):
        return xp.ones(M, dtype=xp.float64, device=device)
    M, needs_trunc = _extend(M, sym)

    n = xp.arange(0, M, dtype=xp.float64, device=device)
    alpha = (M - 1) / 2.0
    w = (special.i0(beta * xp.sqrt(1 - ((n - alpha) / alpha) ** 2.0)) /
         special.i0(xp.asarray(beta, dtype=xp.float64)))

    return _truncate(w, needs_trunc)


def kaiser(M, beta):
    """
    Return the Kaiser window.

    The Kaiser window is a taper formed by using a Bessel function.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero or less, an
        empty array is returned.
    beta : float
        Shape parameter for window.

    Returns
    -------
    out : array
        The window, with the maximum value normalized to one (the value
        one appears only if the number of samples is odd).

    See Also
    --------
    bartlett, blackman, hamming, hanning

    Notes
    -----
    The Kaiser window is defined as

    .. math::  w(n) = I_0\\left( \\beta \\sqrt{1-\\frac{4n^2}{(M-1)^2}}
               \\right)/I_0(\\beta)

    with

    .. math:: \\quad -\\frac{M-1}{2} \\leq n \\leq \\frac{M-1}{2},

    where :math:`I_0` is the modified zeroth-order Bessel function.

    The Kaiser was named for Jim Kaiser, who discovered a simple
    approximation to the DPSS window based on Bessel functions.  The Kaiser
    window is a very good approximation to the Digital Prolate Spheroidal
    Sequence, or Slepian window, which is the transform which maximizes the
    energy in the main lobe of the window relative to total energy.

    The Kaiser can approximate many other windows by varying the beta
    parameter.

    ====  =======================
    beta  Window shape
    ====  =======================
    0     Rectangular
    5     Similar to a Hamming
    6     Similar to a Hanning
    8.6   Similar to a Blackman
    ====  =======================

    A beta value of 14 is probably a good starting point. Note that as beta
    gets large, the window narrows, and so the number of samples needs to be
    large enough to sample the increasingly narrow spike, otherwise NaNs will
    get returned.

    Most references to the Kaiser window come from the signal processing
    literature, where it is used as one of many windowing functions for
    smoothing values.  It is also known as an apodization (which means
    "removing the foot", i.e. smoothing discontinuities at the beginning
    and end of the sampled signal) or tapering function.

    References
    ----------
    .. [1] J. F. Kaiser, "Digital Filters" - Ch 7 in "Systems analysis by
           digital computer", Editors: F.F. Kuo and J.F. Kaiser, p 218-285.
           John Wiley and Sons, New York, (1966).
    .. [2] E.R. Kanasewich, "Time Sequence Analysis in Geophysics", The
           University of Alberta Press, 1975, pp. 177-178.
    .. [3] Wikipedia, "Window function",
           https://en.wikipedia.org/wiki/Window_function

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> np.kaiser(12, 14)
     array([7.72686684e-06, 3.46009194e-03, 4.65200189e-02, # may vary
            2.29737120e-01, 5.99885316e-01, 9.45674898e-01,
            9.45674898e-01, 5.99885316e-01, 2.29737120e-01,
            4.65200189e-02, 3.46009194e-03, 7.72686684e-06])


    Plot the window and the frequency response.

    .. plot::
        :include-source:

        import matplotlib.pyplot as plt
        from numpy.fft import fft, fftshift
        window = np.kaiser(51, 14)
        plt.plot(window)
        plt.title("Kaiser window")
        plt.ylabel("Amplitude")
        plt.xlabel("Sample")
        plt.show()

        plt.figure()
        A = fft(window, 2048) / 25.5
        mag = np.abs(fftshift(A))
        freq = np.linspace(-0.5, 0.5, len(A))
        response = 20 * np.log10(mag)
        response = np.clip(response, -100, 100)
        plt.plot(freq, response)
        plt.title("Frequency response of Kaiser window")
        plt.ylabel("Magnitude [dB]")
        plt.xlabel("Normalized frequency [cycles per sample]")
        plt.axis('tight')
        plt.show()

    """
    # Ensures at least float64 via 0.0.  M should be an integer, but conversion
    # to double is safe for a range.  (Simplified result_type with 0.0
    # strongly typed.  result-type is not/less order sensitive, but that mainly
    # matters for integers anyway.)
    values = np.array([0.0, M, beta])
    M = values[1]
    beta = values[2]

    if M == 1:
        return np.ones(1, dtype=values.dtype)
    n = arange(0, M)
    alpha = (M - 1) / 2.0
    return i0(beta * sqrt(1 - ((n - alpha) / alpha)**2.0)) / i0(beta)


def kaiser(M: int, beta: ArrayLike) -> Array:
  """Return a Kaiser window of size M.

  JAX implementation of :func:`numpy.kaiser`.

  Args:
    M: The window size.
    beta: The Kaiser window parameter.

  Returns:
    An array of size M containing the Kaiser window.

  Examples:
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.kaiser(4, 1.5))
    [0.61 0.95 0.95 0.61]

  See also:
    - :func:`jax.numpy.bartlett`: return a Bartlett window of size M.
    - :func:`jax.numpy.blackman`: return a Blackman window of size M.
    - :func:`jax.numpy.hamming`: return a Hamming window of size M.
    - :func:`jax.numpy.hanning`: return a Hanning window of size M.
  """
  M = core.concrete_or_error(int, M, "M argument of jnp.kaiser")
  dtype = dtypes.default_float_dtype()
  if M <= 1:
    return lax.full((M,), 1, dtype)
  n = lax.iota(dtype, M)
  alpha = 0.5 * (M - 1)
  return lax_numpy.i0(beta * ufuncs.sqrt(1 - ((n - alpha) / alpha) ** 2)) / lax_numpy.i0(beta)

