import math


def cheb2ap(N, rs, *, xp=None, device=None):
    """
    Return (z,p,k) for Nth-order Chebyshev type II analog lowpass filter.

    The returned filter prototype has attenuation of at least ``rs`` decibels
    in the stopband.

    The filter's angular (e.g. rad/s) cutoff frequency is normalized to 1,
    defined as the point at which the attenuation first reaches ``rs``.

    Parameters
    ----------
    N : int
        The order of the filter
    rs : float
        The attenuation in the stopband
    %(xp_device_snippet)s

    Returns
    -------
    z : ndarray[complex128]
        Zeros of the transfer function.
    p : ndarray[complex128]
        Poles of the transfer function.
    k : float
        Gain of the transfer function.

    See Also
    --------
    cheby2 : Filter design function using this prototype

    """
    if xp is None:
        xp = np_compat
    if abs(int(N)) != N:
        raise ValueError("Filter order must be a nonnegative integer")
    elif N == 0:
        # Avoid divide-by-zero warning
        return (
            xp.asarray([], device=device, dtype=xp.complex128),
            xp.asarray([], device=device, dtype=xp.complex128),
            1.0
        )

    # Ripple factor (epsilon)
    de = 1.0 / math.sqrt(10 ** (0.1 * rs) - 1)
    mu = math.asinh(1.0 / de) / N

    if N % 2:
        m = xp.concat(
            (xp.arange(-N + 1, 0, 2, dtype=xp.float64, device=device),
             xp.arange(2, N, 2, dtype=xp.float64, device=device)
            )
        )
    else:
        m = xp.arange(-N+1, N, 2, dtype=xp.float64, device=device)

    z = 1j / xp.sin(m * xp.pi / (2 * N))

    # Poles around the unit circle like Butterworth
    m1 = xp.arange(-N+1, N, 2, dtype=xp.float64, device=device)
    theta1 = xp.pi * m1 / (2 * N)
    p = -1 / xp.sinh(mu + 1j*theta1)

    k = xp.real(xp.prod(-p, axis=0) / xp.prod(-z, axis=0))
    return z, p, k

