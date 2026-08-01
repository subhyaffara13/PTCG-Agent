
def deconvolve(signal, divisor):
    """Deconvolves ``divisor`` out of ``signal`` using inverse filtering.

    Returns the quotient and remainder such that
    ``signal = convolve(divisor, quotient) + remainder``

    Parameters
    ----------
    signal : (N,) array_like
        Signal data, typically a recorded signal
    divisor : (N,) array_like
        Divisor data, typically an impulse response or filter that was
        applied to the original signal

    Returns
    -------
    quotient : ndarray
        Quotient, typically the recovered original signal
    remainder : ndarray
        Remainder

    See Also
    --------
    numpy.polydiv : performs polynomial division (same operation, but
                    also accepts poly1d objects)

    Examples
    --------
    Deconvolve a signal that's been filtered:

    >>> from scipy import signal
    >>> original = [0, 1, 0, 0, 1, 1, 0, 0]
    >>> impulse_response = [2, 1]
    >>> recorded = signal.convolve(impulse_response, original)
    >>> recorded
    array([0, 2, 1, 0, 2, 3, 1, 0, 0])
    >>> recovered, remainder = signal.deconvolve(recorded, impulse_response)
    >>> recovered
    array([ 0.,  1.,  0.,  0.,  1.,  1.,  0.,  0.])
    >>> remainder
    array([0., 0., 0., 0., 0., 0., 0., 0., 0.])
    """
    xp = array_namespace(signal, divisor)

    num = xpx.atleast_nd(xp.asarray(signal), ndim=1, xp=xp)
    den = xpx.atleast_nd(xp.asarray(divisor), ndim=1, xp=xp)
    if not (num.ndim == 1 and xp_size(num) > 0):
        raise ValueError("Parameter signal must be non-empty 1d array, " +
                         f"but its shape is {num.shape}!")
    if not (den.ndim == 1 and xp_size(den) > 0):
        raise ValueError("Parameter divisor must be non-empty 1d array, " +
                         f"but its shape is {den.shape}!")
    N = num.shape[0]
    D = den.shape[0]
    if D > N:
        quot = []
        rem = num
    else:
        input = xp.zeros(N - D + 1, dtype=xp.float64)
        input = xpx.at(input)[0].set(1)
        quot = lfilter(num, den, input)
        rem = num - convolve(den, quot, mode='full')
    return quot, rem

