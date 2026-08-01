
def lanczos(M, *, sym=True, xp=None, device=None):
    r"""Return a Lanczos window also known as a sinc window.

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
    The Lanczos window is defined as

    .. math::  w(n) = sinc \left( \frac{2n}{M - 1} - 1 \right)

    where

    .. math::  sinc(x) = \frac{\sin(\pi x)}{\pi x}

    The Lanczos window has reduced Gibbs oscillations and is widely used for
    filtering climate timeseries with good properties in the physical and
    spectral domains.

    .. versionadded:: 1.10

    References
    ----------
    .. [1] Lanczos, C., and Teichmann, T. (1957). Applied analysis.
           Physics Today, 10, 44.
    .. [2] Duchon C. E. (1979) Lanczos Filtering in One and Two Dimensions.
           Journal of Applied Meteorology, Vol 18, pp 1016-1022.
    .. [3] Thomson, R. E. and Emery, W. J. (2014) Data Analysis Methods in
           Physical Oceanography (Third Edition), Elsevier, pp 593-637.
    .. [4] Wikipedia, "Window function",
           http://en.wikipedia.org/wiki/Window_function

    Examples
    --------
    Plot the window

    >>> import numpy as np
    >>> from scipy.signal.windows import lanczos
    >>> from scipy.fft import fft, fftshift
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots(1)
    >>> window = lanczos(51)
    >>> ax.plot(window)
    >>> ax.set_title("Lanczos window")
    >>> ax.set_ylabel("Amplitude")
    >>> ax.set_xlabel("Sample")
    >>> fig.tight_layout()
    >>> plt.show()

    and its frequency response:

    >>> fig, ax = plt.subplots(1)
    >>> A = fft(window, 2048) / (len(window)/2.0)
    >>> freq = np.linspace(-0.5, 0.5, len(A))
    >>> response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
    >>> ax.plot(freq, response)
    >>> ax.set_xlim(-0.5, 0.5)
    >>> ax.set_ylim(-120, 0)
    >>> ax.set_title("Frequency response of the lanczos window")
    >>> ax.set_ylabel("Normalized magnitude [dB]")
    >>> ax.set_xlabel("Normalized frequency [cycles per sample]")
    >>> fig.tight_layout()
    >>> plt.show()
    """
    xp = _namespace(xp)

    if _len_guards(M):
        return xp.ones(M, dtype=xp.float64, device=device)
    M, needs_trunc = _extend(M, sym)

    # To make sure that the window is symmetric, we concatenate the right hand
    # half of the window and the flipped one which is the left hand half of
    # the window.
    def _calc_right_side_lanczos(n, m):
        return xpx.sinc(2. * xp.arange(n, m, dtype=xp.float64) / (m - 1) - 1.0, xp=xp)

    if M % 2 == 0:
        wh = _calc_right_side_lanczos(M/2, M)
        w = xp.concat([xp.flip(wh), wh])
    else:
        wh = _calc_right_side_lanczos((M+1)/2, M)
        w = xp.concat([xp.flip(wh), xp.ones(1), wh])

    return _truncate(w, needs_trunc)

