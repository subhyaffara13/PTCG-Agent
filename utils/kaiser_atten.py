
def kaiser_atten(numtaps, width):
    """Compute the attenuation of a Kaiser FIR filter.

    Given the number of taps `N` and the transition width `width`, compute the
    attenuation `a` in dB, given by Kaiser's formula:

        a = 2.285 * (N - 1) * pi * width + 7.95

    Parameters
    ----------
    numtaps : int
        The number of taps in the FIR filter.
    width : float
        The desired width of the transition region between passband and
        stopband (or, in general, at any discontinuity) for the filter,
        expressed as a fraction of the Nyquist frequency.

    Returns
    -------
    a : float
        The attenuation of the ripple, in dB.

    See Also
    --------
    kaiserord, kaiser_beta

    Examples
    --------
    Suppose we want to design a FIR filter using the Kaiser window method
    that will have 211 taps and a transition width of 9 Hz for a signal that
    is sampled at 480 Hz. Expressed as a fraction of the Nyquist frequency,
    the width is 9/(0.5*480) = 0.0375. The approximate attenuation (in dB)
    is computed as follows:

    >>> from scipy.signal import kaiser_atten
    >>> kaiser_atten(211, 0.0375)
    64.48099630593983

    """
    a = 2.285 * (numtaps - 1) * np.pi * width + 7.95
    return a

