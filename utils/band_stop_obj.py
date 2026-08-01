
def band_stop_obj(wp, ind, passb, stopb, gpass, gstop, type):
    """
    Band Stop Objective Function for order minimization.

    Returns the non-integer order for an analog band stop filter.

    Parameters
    ----------
    wp : scalar
        Edge of passband `passb`.
    ind : int, {0, 1}
        Index specifying which `passb` edge to vary (0 or 1).
    passb : ndarray
        Two element sequence of fixed passband edges.
    stopb : ndarray
        Two element sequence of fixed stopband edges.
    gpass : float
        Amount of ripple in the passband in dB.
    gstop : float
        Amount of attenuation in stopband in dB.
    type : {'butter', 'cheby', 'ellip'}
        Type of filter.

    Returns
    -------
    n : scalar
        Filter order (possibly non-integer).

    Notes
    -----
    Band-stop filters are used in applications where certain frequency
    components need to be blocked while others are allowed; for instance,
    removing noise at specific frequencies while allowing the desired signal
    to pass through. The order of a filter often determines its complexity and
    accuracy. Determining the right order can be a challenge. This function
    aims to provide an appropriate order for an analog band stop filter.

    Examples
    --------

    >>> import numpy as np
    >>> from scipy.signal import band_stop_obj
    >>> wp = 2
    >>> ind = 1
    >>> passb = np.array([1, 3])
    >>> stopb = np.array([0.5, 4])
    >>> gstop = 30
    >>> gpass = 3
    >>> filter_type = 'butter'
    >>> band_stop_obj(wp, ind, passb, stopb, gpass, gstop, filter_type)
    np.float64(-2.758504160760643)

    """

    _validate_gpass_gstop(gpass, gstop)

    passbC = passb.copy()
    passbC[ind] = wp
    nat = (stopb * (passbC[0] - passbC[1]) /
           (stopb ** 2 - passbC[0] * passbC[1]))
    nat = min(abs(nat))

    if type == 'butter':
        GSTOP = 10 ** (0.1 * abs(gstop))
        GPASS = 10 ** (0.1 * abs(gpass))
        n = (np.log10((GSTOP - 1.0) / (GPASS - 1.0)) / (2 * np.log10(nat)))
    elif type == 'cheby':
        GSTOP = 10 ** (0.1 * abs(gstop))
        GPASS = 10 ** (0.1 * abs(gpass))
        n = np.arccosh(np.sqrt((GSTOP - 1.0) / (GPASS - 1.0))) / np.arccosh(nat)
    elif type == 'ellip':
        GSTOP = 10 ** (0.1 * gstop)
        GPASS = 10 ** (0.1 * gpass)
        arg1 = np.sqrt((GPASS - 1.0) / (GSTOP - 1.0))
        arg0 = 1.0 / nat
        d0 = special.ellipk([arg0 ** 2, 1 - arg0 ** 2])
        d1 = special.ellipk([arg1 ** 2, 1 - arg1 ** 2])
        n = (d0[0] * d1[1] / (d0[1] * d1[0]))
    else:
        raise ValueError(f"Incorrect type: {type}")
    return n

