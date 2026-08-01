
def hamming(M):
    dtype = _dtypes_impl.default_dtypes().float_dtype
    return torch.hamming_window(M, periodic=False, dtype=dtype)


def hamming(
    M: int,
    *,
    sym: bool = True,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: torch.device | None = None,
    requires_grad: bool = False,
) -> Tensor:
    return general_hamming(
        M,
        sym=sym,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )


def hamming(u, v, w=None):
    """
    Compute the Hamming distance between two 1-D arrays.

    The Hamming distance between 1-D arrays `u` and `v`, is simply the
    proportion of disagreeing components in `u` and `v`. If `u` and `v` are
    boolean vectors, the Hamming distance is

    .. math::

       \\frac{c_{01} + c_{10}}{n}

    where :math:`c_{ij}` is the number of occurrences of
    :math:`\\mathtt{u[k]} = i` and :math:`\\mathtt{v[k]} = j` for
    :math:`k < n`.

    Parameters
    ----------
    u : (N,) array_like
        Input array.
    v : (N,) array_like
        Input array.
    w : (N,) array_like, optional
        The weights for each value in `u` and `v`. Default is None,
        which gives each value a weight of 1.0

    Returns
    -------
    hamming : double
        The Hamming distance between vectors `u` and `v`.

    Examples
    --------
    >>> from scipy.spatial import distance
    >>> distance.hamming([1, 0, 0], [0, 1, 0])
    0.66666666666666663
    >>> distance.hamming([1, 0, 0], [1, 1, 0])
    0.33333333333333331
    >>> distance.hamming([1, 0, 0], [2, 0, 0])
    0.33333333333333331
    >>> distance.hamming([1, 0, 0], [3, 0, 0])
    0.33333333333333331

    """
    u = _validate_vector(u)
    v = _validate_vector(v)
    if u.shape != v.shape:
        raise ValueError('The 1d arrays must have equal lengths.')
    u_ne_v = u != v
    if w is not None:
        w = _validate_weights(w)
        if w.shape != u.shape:
            raise ValueError("'w' should have the same length as 'u' and 'v'.")
        w = w / w.sum()
        return np.dot(u_ne_v, w)
    return np.mean(u_ne_v)


def hamming(M, sym=True, *, xp=None, device=None):
    r"""Return a Hamming window.

    The Hamming window is a taper formed by using a raised cosine with
    non-zero endpoints, optimized to minimize the nearest side lobe.

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
    The Hamming window is defined as

    .. math::  w(n) = 0.54 - 0.46 \cos\left(\frac{2\pi{n}}{M-1}\right)
               \qquad 0 \leq n \leq M-1

    The Hamming was named for R. W. Hamming, an associate of J. W. Tukey and
    is described in Blackman and Tukey. It was recommended for smoothing the
    truncated autocovariance function in the time domain.
    Most references to the Hamming window come from the signal processing
    literature, where it is used as one of many windowing functions for
    smoothing values.  It is also known as an apodization (which means
    "removing the foot", i.e. smoothing discontinuities at the beginning
    and end of the sampled signal) or tapering function.

    References
    ----------
    .. [1] Blackman, R.B. and Tukey, J.W., (1958) The measurement of power
           spectra, Dover Publications, New York.
    .. [2] E.R. Kanasewich, "Time Sequence Analysis in Geophysics", The
           University of Alberta Press, 1975, pp. 109-110.
    .. [3] Wikipedia, "Window function",
           https://en.wikipedia.org/wiki/Window_function
    .. [4] W.H. Press,  B.P. Flannery, S.A. Teukolsky, and W.T. Vetterling,
           "Numerical Recipes", Cambridge University Press, 1986, page 425.

    Examples
    --------
    Plot the window and its frequency response:

    >>> import numpy as np
    >>> from scipy import signal
    >>> from scipy.fft import fft, fftshift
    >>> import matplotlib.pyplot as plt

    >>> window = signal.windows.hamming(51)
    >>> plt.plot(window)
    >>> plt.title("Hamming window")
    >>> plt.ylabel("Amplitude")
    >>> plt.xlabel("Sample")

    >>> plt.figure()
    >>> A = fft(window, 2048) / (len(window)/2.0)
    >>> freq = np.linspace(-0.5, 0.5, len(A))
    >>> response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
    >>> plt.plot(freq, response)
    >>> plt.axis([-0.5, 0.5, -120, 0])
    >>> plt.title("Frequency response of the Hamming window")
    >>> plt.ylabel("Normalized magnitude [dB]")
    >>> plt.xlabel("Normalized frequency [cycles per sample]")

    """
    # Docstring adapted from NumPy's hamming function
    return general_hamming(M, 0.54, sym, xp=xp, device=device)


def hamming(M):
    """
    Return the Hamming window.

    The Hamming window is a taper formed by using a weighted cosine.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero or less, an
        empty array is returned.

    Returns
    -------
    out : ndarray
        The window, with the maximum value normalized to one (the value
        one appears only if the number of samples is odd).

    See Also
    --------
    bartlett, blackman, hanning, kaiser

    Notes
    -----
    The Hamming window is defined as

    .. math::  w(n) = 0.54 - 0.46\\cos\\left(\\frac{2\\pi{n}}{M-1}\\right)
               \\qquad 0 \\leq n \\leq M-1

    The Hamming was named for R. W. Hamming, an associate of J. W. Tukey
    and is described in Blackman and Tukey. It was recommended for
    smoothing the truncated autocovariance function in the time domain.
    Most references to the Hamming window come from the signal processing
    literature, where it is used as one of many windowing functions for
    smoothing values.  It is also known as an apodization (which means
    "removing the foot", i.e. smoothing discontinuities at the beginning
    and end of the sampled signal) or tapering function.

    References
    ----------
    .. [1] Blackman, R.B. and Tukey, J.W., (1958) The measurement of power
           spectra, Dover Publications, New York.
    .. [2] E.R. Kanasewich, "Time Sequence Analysis in Geophysics", The
           University of Alberta Press, 1975, pp. 109-110.
    .. [3] Wikipedia, "Window function",
           https://en.wikipedia.org/wiki/Window_function
    .. [4] W.H. Press,  B.P. Flannery, S.A. Teukolsky, and W.T. Vetterling,
           "Numerical Recipes", Cambridge University Press, 1986, page 425.

    Examples
    --------
    >>> import numpy as np
    >>> np.hamming(12)
    array([ 0.08      ,  0.15302337,  0.34890909,  0.60546483,  0.84123594, # may vary
            0.98136677,  0.98136677,  0.84123594,  0.60546483,  0.34890909,
            0.15302337,  0.08      ])

    Plot the window and the frequency response.

    .. plot::
        :include-source:

        import matplotlib.pyplot as plt
        from numpy.fft import fft, fftshift
        window = np.hamming(51)
        plt.plot(window)
        plt.title("Hamming window")
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
        plt.title("Frequency response of Hamming window")
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
    return 0.54 + 0.46 * cos(pi * n / (M - 1))


def hamming(M: int) -> Array:
  """Return a Hamming window of size M.

  JAX implementation of :func:`numpy.hamming`.

  Args:
    M: The window size.

  Returns:
    An array of size M containing the Hamming window.

  Examples:
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.hamming(4))
    [0.08 0.77 0.77 0.08]

  See also:
    - :func:`jax.numpy.bartlett`: return a Bartlett window of size M.
    - :func:`jax.numpy.blackman`: return a Blackman window of size M.
    - :func:`jax.numpy.hanning`: return a Hanning window of size M.
    - :func:`jax.numpy.kaiser`: return a Kaiser window of size M.
  """
  M = core.concrete_or_error(int, M, "M argument of jnp.hamming")
  dtype = dtypes.default_float_dtype()
  if M <= 1:
    return lax.full((M,), 1, dtype)
  n = lax.iota(dtype, M)
  return 0.54 - 0.46 * ufuncs.cos(2 * np.pi * n / (M - 1))

