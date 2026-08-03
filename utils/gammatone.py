import math


def gammatone(freq, ftype, order=None, numtaps=None, fs=None, *, xp=None, device=None):
    """
    Gammatone filter design.

    This function computes the coefficients of an FIR or IIR gammatone
    digital filter [1]_.

    Parameters
    ----------
    freq : float
        Center frequency of the filter (expressed in the same units
        as `fs`).
    ftype : {'fir', 'iir'}
        The type of filter the function generates. If 'fir', the function
        will generate an Nth order FIR gammatone filter. If 'iir', the
        function will generate an 8th order digital IIR filter, modeled as
        as 4th order gammatone filter.
    order : int, optional
        The order of the filter. Only used when ``ftype='fir'``.
        Default is 4 to model the human auditory system. Must be between
        0 and 24.
    numtaps : int, optional
        Length of the filter. Only used when ``ftype='fir'``.
        Default is ``fs*0.015`` if `fs` is greater than 1000,
        15 if `fs` is less than or equal to 1000.
    fs : float, optional
        The sampling frequency of the signal. `freq` must be between
        0 and ``fs/2``. Default is 2.
    %(xp_device_snippet)s

    Returns
    -------
    b, a : ndarray, ndarray
        Numerator (``b``) and denominator (``a``) polynomials of the filter.

    Raises
    ------
    ValueError
        If `freq` is less than or equal to 0 or greater than or equal to
        ``fs/2``, if `ftype` is not 'fir' or 'iir', if `order` is less than
        or equal to 0 or greater than 24 when ``ftype='fir'``

    See Also
    --------
    firwin
    iirfilter

    References
    ----------
    .. [1] Slaney, Malcolm, "An Efficient Implementation of the
        Patterson-Holdsworth Auditory Filter Bank", Apple Computer
        Technical Report 35, 1993, pp.3-8, 34-39.

    Examples
    --------
    16-sample 4th order FIR Gammatone filter centered at 440 Hz

    >>> from scipy import signal
    >>> signal.gammatone(440, 'fir', numtaps=16, fs=16000)
    (array([ 0.00000000e+00,  2.22196719e-07,  1.64942101e-06,  4.99298227e-06,
        1.01993969e-05,  1.63125770e-05,  2.14648940e-05,  2.29947263e-05,
        1.76776931e-05,  2.04980537e-06, -2.72062858e-05, -7.28455299e-05,
       -1.36651076e-04, -2.19066855e-04, -3.18905076e-04, -4.33156712e-04]),
       [1.0])

    IIR Gammatone filter centered at 440 Hz

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np

    >>> fc, fs = 440, 16000
    >>> b, a = signal.gammatone(fc, 'iir', fs=fs)
    >>> w, h = signal.freqz(b, a)
    >>> plt.plot(w * fs / (2 * np.pi), 20 * np.log10(abs(h)))
    >>> plt.xscale('log')
    >>> plt.title('Gammatone filter frequency response')
    >>> plt.xlabel('Frequency [Hz]')
    >>> plt.ylabel('Amplitude [dB]')
    >>> plt.margins(0, 0.1)
    >>> plt.grid(which='both', axis='both')
    >>> plt.axvline(fc, color='green') # cutoff frequency
    >>> plt.show()
    """
    if xp is None:
        xp = np_compat

    # Converts freq to float
    freq = float(freq)

    # Set sampling rate if not passed
    if fs is None:
        fs = 2
    fs = _validate_fs(fs, allow_none=False)

    # Check for invalid cutoff frequency or filter type
    ftype = ftype.lower()
    filter_types = ['fir', 'iir']
    if not 0 < freq < fs / 2:
        raise ValueError(f"The frequency must be between 0 and {fs / 2}"
                         f" (Nyquist), but given {freq}.")
    if ftype not in filter_types:
        raise ValueError('ftype must be either fir or iir.')

    # Calculate FIR gammatone filter
    if ftype == 'fir':
        # Set order and numtaps if not passed
        if order is None:
            order = 4
        order = operator.index(order)

        if numtaps is None:
            numtaps = max(int(fs * 0.015), 15)
        numtaps = operator.index(numtaps)

        # Check for invalid order
        if not 0 < order <= 24:
            raise ValueError("Invalid order: order must be > 0 and <= 24.")

        # Gammatone impulse response settings
        t = xp.arange(numtaps, device=device, dtype=xp_default_dtype(xp)) / fs
        bw = 1.019 * _hz_to_erb(freq)

        # Calculate the FIR gammatone filter
        b = (t ** (order - 1)) * xp.exp(-2 * xp.pi * bw * t)
        b = b * xp.cos(2 * xp.pi * freq * t)

        # Scale the FIR filter so the frequency response is 1 at cutoff
        scale_factor = 2 * (2 * xp.pi * bw) ** (order)
        scale_factor /= float_factorial(order - 1)
        scale_factor /= fs
        b = b * scale_factor
        a = xp.asarray([1.0], device=device)

    # Calculate IIR gammatone filter
    elif ftype == 'iir':
        # Raise warning if order and/or numtaps is passed
        if order is not None:
            warnings.warn('order is not used for IIR gammatone filter.', stacklevel=2)
        if numtaps is not None:
            warnings.warn('numtaps is not used for IIR gammatone filter.', stacklevel=2)

        # Gammatone impulse response settings
        T = 1./fs
        bw = 2 * math.pi * 1.019 * _hz_to_erb(freq)
        fr = 2 * freq * math.pi * T
        bwT = bw * T

        # Calculate the gain to normalize the volume at the center frequency
        g1 = -2 * cmath.exp(2j * fr) * T
        g2 = 2 * cmath.exp(-(bwT) + 1j * fr) * T
        g3 = math.sqrt(3 + 2 ** (3 / 2)) * math.sin(fr)
        g4 = math.sqrt(3 - 2 ** (3 / 2)) * math.sin(fr)
        g5 = cmath.exp(2j * fr)

        g = g1 + g2 * (math.cos(fr) - g4)
        g *= (g1 + g2 * (math.cos(fr) + g4))
        g *= (g1 + g2 * (math.cos(fr) - g3))
        g *= (g1 + g2 * (math.cos(fr) + g3))
        g /= ((-2 / math.exp(2 * bwT) - 2 * g5 + 2 * (1 + g5) / math.exp(bwT)) ** 4)
        g = math.hypot(g.real, g.imag)

        # Create empty filter coefficient lists
        b = [None] * 5  #np.empty(5)
        a = [None] * 9  # np.empty(9)

        # Calculate the numerator coefficients
        b[0] = (T ** 4) / g
        b[1] = -4 * T ** 4 * math.cos(fr) / math.exp(bw * T) / g
        b[2] = 6 * T ** 4 * math.cos(2 * fr) / math.exp(2 * bw * T) / g
        b[3] = -4 * T ** 4 * math.cos(3 * fr) / math.exp(3 * bw * T) / g
        b[4] = T ** 4 * math.cos(4 * fr) / math.exp(4 * bw * T) / g

        # Calculate the denominator coefficients
        a[0] = 1
        a[1] = -8 * math.cos(fr) / math.exp(bw * T)
        a[2] = 4 * (4 + 3 * math.cos(2 * fr)) / math.exp(2 * bw * T)
        a[3] = -8 * (6 * math.cos(fr) + math.cos(3 * fr))
        a[3] /= math.exp(3 * bw * T)
        a[4] = 2 * (18 + 16 * math.cos(2 * fr) + math.cos(4 * fr))
        a[4] /= math.exp(4 * bw * T)
        a[5] = -8 * (6 * math.cos(fr) + math.cos(3 * fr))
        a[5] /= math.exp(5 * bw * T)
        a[6] = 4 * (4 + 3 * math.cos(2 * fr)) / math.exp(6 * bw * T)
        a[7] = -8 * math.cos(fr) / math.exp(7 * bw * T)
        a[8] = math.exp(-8 * bw * T)

    return xp.asarray(b, device=device), xp.asarray(a, device=device)

