
def blackman(M):
    dtype = _dtypes_impl.default_dtypes().float_dtype
    return torch.blackman_window(M, periodic=False, dtype=dtype)


def blackman(
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

    _window_function_checks("blackman", M, dtype, layout)

    return general_cosine(
        M,
        a=[0.42, 0.5, 0.08],
        sym=sym,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )


def blackman(M, sym=True, *, xp=None, device=None):
    r"""
    Return a Blackman window.

    The Blackman window is a taper formed by using the first three terms of
    a summation of cosines. It was designed to have close to the minimal
    leakage possible.  It is close to optimal, only slightly worse than a
    Kaiser window.

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
        The window, with the maximum value normalized to 1 (though the value 1
        does not appear if `M` is even and `sym` is True).

    Notes
    -----
    The Blackman window is defined as

    .. math::  w(n) = 0.42 - 0.5 \cos(2\pi n/M) + 0.08 \cos(4\pi n/M)

    The "exact Blackman" window was designed to null out the third and fourth
    sidelobes, but has discontinuities at the boundaries, resulting in a
    6 dB/oct fall-off.  This window is an approximation of the "exact" window,
    which does not null the sidelobes as well, but is smooth at the edges,
    improving the fall-off rate to 18 dB/oct. [3]_

    Most references to the Blackman window come from the signal processing
    literature, where it is used as one of many windowing functions for
    smoothing values.  It is also known as an apodization (which means
    "removing the foot", i.e. smoothing discontinuities at the beginning
    and end of the sampled signal) or tapering function. It is known as a
    "near optimal" tapering function, almost as good (by some measures)
    as the Kaiser window.

    References
    ----------
    .. [1] Blackman, R.B. and Tukey, J.W., (1958) The measurement of power
           spectra, Dover Publications, New York.
    .. [2] Oppenheim, A.V., and R.W. Schafer. Discrete-Time Signal Processing.
           Upper Saddle River, NJ: Prentice-Hall, 1999, pp. 468-471.
    .. [3] Harris, Fredric J. (Jan 1978). "On the use of Windows for Harmonic
           Analysis with the Discrete Fourier Transform". Proceedings of the
           IEEE 66 (1): 51-83. :doi:`10.1109/PROC.1978.10837`.

    Examples
    --------
    Plot the window and its frequency response:

    >>> import numpy as np
    >>> from scipy import signal
    >>> from scipy.fft import fft, fftshift
    >>> import matplotlib.pyplot as plt

    >>> window = signal.windows.blackman(51)
    >>> plt.plot(window)
    >>> plt.title("Blackman window")
    >>> plt.ylabel("Amplitude")
    >>> plt.xlabel("Sample")

    >>> plt.figure()
    >>> A = fft(window, 2048) / (len(window)/2.0)
    >>> freq = np.linspace(-0.5, 0.5, len(A))
    >>> response = np.abs(fftshift(A / abs(A).max()))
    >>> response = 20 * np.log10(np.maximum(response, 1e-10))
    >>> plt.plot(freq, response)
    >>> plt.axis([-0.5, 0.5, -120, 0])
    >>> plt.title("Frequency response of the Blackman window")
    >>> plt.ylabel("Normalized magnitude [dB]")
    >>> plt.xlabel("Normalized frequency [cycles per sample]")

    """
    # Docstring adapted from NumPy's blackman function
    xp = _namespace(xp)
    a = xp.asarray([0.42, 0.50, 0.08], dtype=xp.float64, device=device)
    device = xp_device(a)
    return _general_cosine_impl(M, a, xp, device, sym=sym)


def blackman(M):
    """
    Return the Blackman window.

    The Blackman window is a taper formed by using the first three
    terms of a summation of cosines. It was designed to have close to the
    minimal leakage possible.  It is close to optimal, only slightly worse
    than a Kaiser window.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero or less, an empty
        array is returned.

    Returns
    -------
    out : ndarray
        The window, with the maximum value normalized to one (the value one
        appears only if the number of samples is odd).

    See Also
    --------
    bartlett, hamming, hanning, kaiser

    Notes
    -----
    The Blackman window is defined as

    .. math::  w(n) = 0.42 - 0.5 \\cos(2\\pi n/M) + 0.08 \\cos(4\\pi n/M)

    Most references to the Blackman window come from the signal processing
    literature, where it is used as one of many windowing functions for
    smoothing values.  It is also known as an apodization (which means
    "removing the foot", i.e. smoothing discontinuities at the beginning
    and end of the sampled signal) or tapering function. It is known as a
    "near optimal" tapering function, almost as good (by some measures)
    as the Kaiser window.

    References
    ----------
    .. [1] Blackman, R.B. and Tukey, J.W., (1958)
           The measurement of power spectra, Dover Publications, New York.
    .. [2] Oppenheim, A.V., and R.W. Schafer. Discrete-Time Signal Processing.
           Upper Saddle River, NJ: Prentice-Hall, 1999, pp. 468-471.

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> np.blackman(12)
    array([-1.38777878e-17,   3.26064346e-02,   1.59903635e-01, # may vary
            4.14397981e-01,   7.36045180e-01,   9.67046769e-01,
            9.67046769e-01,   7.36045180e-01,   4.14397981e-01,
            1.59903635e-01,   3.26064346e-02,  -1.38777878e-17])

    Plot the window and the frequency response.

    .. plot::
        :include-source:

        import matplotlib.pyplot as plt
        from numpy.fft import fft, fftshift
        window = np.blackman(51)
        plt.plot(window)
        plt.title("Blackman window")
        plt.ylabel("Amplitude")
        plt.xlabel("Sample")
        plt.show()  # doctest: +SKIP

        plt.figure()
        A = fft(window, 2048) / 25.5
        mag = np.abs(fftshift(A))
        freq = np.linspace(-0.5, 0.5, len(A))
        with np.errstate(divide='ignore', invalid='ignore'):
            response = 20 * np.log10(mag)
        response = np.clip(response, -100, 100)
        plt.plot(freq, response)
        plt.title("Frequency response of Blackman window")
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
    return 0.42 + 0.5 * cos(pi * n / (M - 1)) + 0.08 * cos(2.0 * pi * n / (M - 1))


def blackman(M: int) -> Array:
  """Return a Blackman window of size M.

  JAX implementation of :func:`numpy.blackman`.

  Args:
    M: The window size.

  Returns:
    An array of size M containing the Blackman window.

  Examples:
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.blackman(4))
    [-0.    0.63  0.63 -0.  ]

  See also:
    - :func:`jax.numpy.bartlett`: return a Bartlett window of size M.
    - :func:`jax.numpy.hamming`: return a Hamming window of size M.
    - :func:`jax.numpy.hanning`: return a Hanning window of size M.
    - :func:`jax.numpy.kaiser`: return a Kaiser window of size M.
  """
  M = core.concrete_or_error(int, M, "M argument of jnp.blackman")
  dtype = dtypes.default_float_dtype()
  if M <= 1:
    return lax.full((M,), 1, dtype)
  n = lax.iota(dtype, M)
  return 0.42 - 0.5 * ufuncs.cos(2 * np.pi * n / (M - 1)) + 0.08 * ufuncs.cos(4 * np.pi * n / (M - 1))

