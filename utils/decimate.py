
def decimate(x, q, n=None, ftype='iir', axis=-1, zero_phase=True):
    """
    Downsample the signal after applying an anti-aliasing filter.

    By default, an order 8 Chebyshev type I filter is used. A 30 point FIR
    filter with Hamming window is used if `ftype` is 'fir'.

    Parameters
    ----------
    x : array_like
        The input signal made up of equidistant samples. If `x` is a multidimensional
        array, the parameter `axis` specifies the time axis.
    q : int
        The downsampling factor, which is a postive integer. When using IIR
        downsampling, it is recommended to call `decimate` multiple times for
        downsampling factors higher than 13.
    n : int, optional
        The order of the filter (1 less than the length for 'fir'). Defaults to
        8 for 'iir' and 20 times the downsampling factor for 'fir'.
    ftype : str {'iir', 'fir'} or ``dlti`` instance, optional
        If 'iir' or 'fir', specifies the type of lowpass filter. If an instance
        of an `dlti` object, uses that object to filter before downsampling.
    axis : int, optional
        The axis along which to decimate.
    zero_phase : bool, optional
        Prevent phase shift by filtering with `filtfilt` instead of `lfilter`
        when using an IIR filter, and shifting the outputs back by the filter's
        group delay when using an FIR filter. The default value of ``True`` is
        recommended, since a phase shift is generally not desired.

        .. versionadded:: 0.18.0

    Returns
    -------
    y : ndarray
        The down-sampled signal.

    See Also
    --------
    resample : Resample up or down using the FFT method.
    resample_poly : Resample using polyphase filtering and an FIR filter.

    Notes
    -----
    For non-integer downsampling factors, `~scipy.signal.resample` can be used. Consult
    the `scipy.interpolate` module for methods of resampling signals with non-constant
    sampling intervals.

    The ``zero_phase`` keyword was added in 0.18.0.
    The possibility to use instances of ``dlti`` as ``ftype`` was added in
    0.18.0.

    Examples
    --------

    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt

    Define wave parameters.

    >>> wave_duration = 3
    >>> sample_rate = 100
    >>> freq = 2
    >>> q = 5

    Calculate number of samples.

    >>> samples = wave_duration*sample_rate
    >>> samples_decimated = int(samples/q)

    Create cosine wave.

    >>> x = np.linspace(0, wave_duration, samples, endpoint=False)
    >>> y = np.cos(x*np.pi*freq*2)

    Decimate cosine wave.

    >>> ydem = signal.decimate(y, q)
    >>> xnew = np.linspace(0, wave_duration, samples_decimated, endpoint=False)

    Plot original and decimated waves.

    >>> plt.plot(x, y, '.-', xnew, ydem, 'o-')
    >>> plt.xlabel('Time, Seconds')
    >>> plt.legend(['data', 'decimated'], loc='best')
    >>> plt.show()

    """

    x = np.asarray(x)
    q = operator.index(q)

    if n is not None:
        n = operator.index(n)

    result_type = x.dtype
    if not np.issubdtype(result_type, np.inexact) \
       or result_type.type == np.float16:
        # upcast integers and float16 to float64
        result_type = np.float64

    if ftype == 'fir':
        if n is None:
            half_len = 10 * q  # reasonable cutoff for our sinc-like function
            n = 2 * half_len
        b, a = firwin(n+1, 1. / q, window='hamming'), 1.
        b = np.asarray(b, dtype=result_type)
        a = np.asarray(a, dtype=result_type)
    elif ftype == 'iir':
        iir_use_sos = True
        if n is None:
            n = 8
        sos = cheby1(n, 0.05, 0.8 / q, output='sos')
        sos = np.asarray(sos, dtype=result_type)
    elif isinstance(ftype, dlti):
        system = ftype._as_zpk()
        if system.poles.shape[0] == 0:
            # FIR
            system = ftype._as_tf()
            b, a = system.num, system.den
            ftype = 'fir'
        elif (any(np.iscomplex(system.poles))
              or any(np.iscomplex(system.poles))
              or np.iscomplex(system.gain)):
            # sosfilt & sosfiltfilt don't handle complex coeffs
            iir_use_sos = False
            system = ftype._as_tf()
            b, a = system.num, system.den
        else:
            iir_use_sos = True
            sos = zpk2sos(system.zeros, system.poles, system.gain)
            sos = np.asarray(sos, dtype=result_type)
    else:
        raise ValueError('invalid ftype')

    sl = [slice(None)] * x.ndim

    if ftype == 'fir':
        b = b / a
        if zero_phase:
            y = resample_poly(x, 1, q, axis=axis, window=b)
        else:
            # upfirdn is generally faster than lfilter by a factor equal to the
            # downsampling factor, since it only calculates the needed outputs
            n_out = x.shape[axis] // q + bool(x.shape[axis] % q)
            y = upfirdn(b, x, up=1, down=q, axis=axis)
            sl[axis] = slice(None, n_out, None)

    else:  # IIR case
        if zero_phase:
            if iir_use_sos:
                y = sosfiltfilt(sos, x, axis=axis)
            else:
                y = filtfilt(b, a, x, axis=axis)
        else:
            if iir_use_sos:
                y = sosfilt(sos, x, axis=axis)
            else:
                y = lfilter(b, a, x, axis=axis)

        sl[axis] = slice(None, None, q)

    return y[tuple(sl)]

