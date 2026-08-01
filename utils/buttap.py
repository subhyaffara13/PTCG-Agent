
def buttap(N, *, xp=None, device=None):
    """Return (z,p,k) for analog prototype of Nth-order Butterworth filter.

    The filter will have an angular (e.g., rad/s) cutoff frequency of 1.

    Parameters
    ----------
    N : int
        The order of the filter
    %(xp_device_snippet)s

    Returns
    -------
    z : ndarray[float64]
        Zeros of the transfer function. Is always an empty array.
    p : ndarray[complex128]
        Poles of the transfer function.
    k : float
        Gain of the transfer function.

    See Also
    --------
    butter : Filter design function using this prototype

    """
    if xp is None:
        xp = np_compat
    if abs(int(N)) != N:
        raise ValueError("Filter order must be a nonnegative integer")
    z = xp.asarray([], device=device, dtype=xp.float64)
    m = xp.arange(-N+1, N, 2, device=device, dtype=xp.float64)
    # Middle value is 0 to ensure an exactly real pole
    p = -xp.exp(1j * xp.pi * m / (2 * N))
    k = 1.0
    return z, p, k

