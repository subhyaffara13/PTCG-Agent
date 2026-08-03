import math


def cheb1ap(N, rp, *, xp=None, device=None):
    """
    Return (z,p,k) for Nth-order Chebyshev type I analog lowpass filter.

    The returned filter prototype has `rp` decibels of ripple in the passband.

    The filter's angular (e.g. rad/s) cutoff frequency is normalized to 1,
    defined as the point at which the gain first drops below ``-rp``.

    Parameters
    ----------
    N : int
        The order of the filter
    rp : float
        The ripple intensity
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
    cheby1 : Filter design function using this prototype

    """
    if xp is None:
        xp = np_compat
    if abs(int(N)) != N:
        raise ValueError("Filter order must be a nonnegative integer")
    elif N == 0:
        # Avoid divide-by-zero error
        # Even order filters have DC gain of -rp dB
        return (
            xp.asarray([], device=device, dtype=xp.float64),
            xp.asarray([], device=device, dtype=xp.complex128), 10**(-rp/20)
        )
    z = xp.asarray([], device=device, dtype=xp.float64)

    # Ripple factor (epsilon)
    eps = math.sqrt(10 ** (0.1 * rp) - 1.0)
    mu = 1.0 / N * math.asinh(1 / eps)

    # Arrange poles in an ellipse on the left half of the S-plane
    m = xp.arange(-N+1, N, 2, dtype=xp.float64, device=device)
    theta = xp.pi * m / (2*N)
    p = -xp.sinh(mu + 1j*theta)

    k = xp.real(xp.prod(-p, axis=0))
    if N % 2 == 0:
        k = k / math.sqrt(1 + eps * eps)

    return z, p, k

