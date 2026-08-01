
def kaiser_bessel_derived(M, beta, *, sym=True, xp=None, device=None):
    """Return a Kaiser-Bessel derived window.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero, an empty array
        is returned. An exception is thrown when it is negative.
        Note that this window is only defined for an even
        number of points.
    beta : float
        Kaiser window shape parameter.
    sym : bool, optional
        This parameter only exists to comply with the interface offered by
        the other window functions and to be callable by `get_window`.
        When True (default), generates a symmetric window, for use in filter
        design.
    %(xp_device_snippet)s

    Returns
    -------
    w : ndarray
        The window, normalized to fulfil the Princen-Bradley condition.

    See Also
    --------
    kaiser

    Notes
    -----
    It is designed to be suitable for use with the modified discrete cosine
    transform (MDCT) and is mainly used in audio signal processing and
    audio coding.

    .. versionadded:: 1.9.0

    References
    ----------
    .. [1] Bosi, Marina, and Richard E. Goldberg. Introduction to Digital
           Audio Coding and Standards. Dordrecht: Kluwer, 2003.
    .. [2] Wikipedia, "Kaiser window",
           https://en.wikipedia.org/wiki/Kaiser_window

    Examples
    --------
    Plot the Kaiser-Bessel derived window based on the wikipedia
    reference [2]_:

    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
    >>> N = 50
    >>> for alpha in [0.64, 2.55, 7.64, 31.83]:
    ...     ax.plot(signal.windows.kaiser_bessel_derived(2*N, np.pi*alpha),
    ...             label=f"{alpha=}")
    >>> ax.grid(True)
    >>> ax.set_title("Kaiser-Bessel derived window")
    >>> ax.set_ylabel("Amplitude")
    >>> ax.set_xlabel("Sample")
    >>> ax.set_xticks([0, N, 2*N-1])
    >>> ax.set_xticklabels(["0", "N", "2N+1"])  # doctest: +SKIP
    >>> ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.707, 0.8, 1.0])
    >>> fig.legend(loc="center")
    >>> fig.tight_layout()
    >>> fig.show()
    """
    xp = _namespace(xp)

    if not sym:
        raise ValueError(
            "Kaiser-Bessel Derived windows are only defined for symmetric "
            "shapes"
        )
    elif M < 1:
        return xp.asarray([])
    elif M % 2:
        raise ValueError(
            "Kaiser-Bessel Derived windows are only defined for even number "
            "of points"
        )

    kaiser_window = kaiser(M // 2 + 1, beta, xp=xp, device=device)
    csum = xp.cumulative_sum(kaiser_window)
    half_window = xp.sqrt(csum[:-1] / csum[-1])
    w = xp.concat((half_window, xp.flip(half_window)), axis=0)
    return xp.asarray(w, device=device)

