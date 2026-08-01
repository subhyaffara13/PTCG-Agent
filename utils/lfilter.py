
def lfilter(b, a, x, axis=-1, zi=None):
    """
    Filter data along one-dimension with an IIR or FIR filter.

    Filter a data sequence, `x`, using a digital filter.  This works for many
    fundamental data types (including Object type).  The filter is a direct
    form II transposed implementation of the standard difference equation
    (see Notes).

    The function `sosfilt` (and filter design using ``output='sos'``) should be
    preferred over `lfilter` for most filtering tasks, as second-order sections
    have fewer numerical problems.

    Parameters
    ----------
    b : array_like
        The numerator coefficient vector in a 1-D sequence.
    a : array_like
        The denominator coefficient vector in a 1-D sequence.  If ``a[0]``
        is not 1, then both `a` and `b` are normalized by ``a[0]``.
    x : array_like
        An N-dimensional input array.
    axis : int, optional
        The axis of the input data array along which to apply the
        linear filter. The filter is applied to each subarray along
        this axis.  Default is -1.
    zi : array_like, optional
        Initial conditions for the filter delays.  It is a vector
        (or array of vectors for an N-dimensional input) of length
        ``max(len(a), len(b)) - 1``.  If `zi` is None or is not given then
        initial rest is assumed.  See `lfiltic` for more information.

    Returns
    -------
    y : array
        The output of the digital filter.
    zf : array, optional
        If `zi` is None, this is not returned, otherwise, `zf` holds the
        final filter delay values.

    See Also
    --------
    lfiltic : Construct initial conditions for `lfilter`.
    lfilter_zi : Compute initial state (steady state of step response) for
                 `lfilter`.
    filtfilt : A forward-backward filter, to obtain a filter with zero phase.
    savgol_filter : A Savitzky-Golay filter.
    sosfilt: Filter data using cascaded second-order sections.
    sosfiltfilt: A forward-backward filter using second-order sections.

    Notes
    -----
    The filter function is implemented as a direct II transposed structure.
    This means that the filter implements::

       a[0]*y[n] = b[0]*x[n] + b[1]*x[n-1] + ... + b[M]*x[n-M]
                             - a[1]*y[n-1] - ... - a[N]*y[n-N]

    where `M` is the degree of the numerator, `N` is the degree of the
    denominator, and `n` is the sample number.  It is implemented using
    the following difference equations (assuming M = N)::

         a[0]*y[n] = b[0] * x[n]               + d[0][n-1]
           d[0][n] = b[1] * x[n] - a[1] * y[n] + d[1][n-1]
           d[1][n] = b[2] * x[n] - a[2] * y[n] + d[2][n-1]
         ...
         d[N-2][n] = b[N-1]*x[n] - a[N-1]*y[n] + d[N-1][n-1]
         d[N-1][n] = b[N] * x[n] - a[N] * y[n]

    where `d` are the state variables.

    The rational transfer function describing this filter in the
    z-transform domain is::

                             -1              -M
                 b[0] + b[1]z  + ... + b[M] z
         Y(z) = -------------------------------- X(z)
                             -1              -N
                 a[0] + a[1]z  + ... + a[N] z

    Examples
    --------
    Generate a noisy signal to be filtered:

    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> rng = np.random.default_rng()
    >>> t = np.linspace(-1, 1, 201)
    >>> x = (np.sin(2*np.pi*0.75*t*(1-t) + 2.1) +
    ...      0.1*np.sin(2*np.pi*1.25*t + 1) +
    ...      0.18*np.cos(2*np.pi*3.85*t))
    >>> xn = x + rng.standard_normal(len(t)) * 0.08

    Create an order 3 lowpass butterworth filter:

    >>> b, a = signal.butter(3, 0.05)

    Apply the filter to xn.  Use lfilter_zi to choose the initial condition of
    the filter:

    >>> zi = signal.lfilter_zi(b, a)
    >>> z, _ = signal.lfilter(b, a, xn, zi=zi*xn[0])

    Apply the filter again, to have a result filtered at an order the same as
    filtfilt:

    >>> z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])

    Use filtfilt to apply the filter:

    >>> y = signal.filtfilt(b, a, xn)

    Plot the original signal and the various filtered versions:

    >>> plt.figure
    >>> plt.plot(t, xn, 'b', alpha=0.75)
    >>> plt.plot(t, z, 'r--', t, z2, 'r', t, y, 'k')
    >>> plt.legend(('noisy signal', 'lfilter, once', 'lfilter, twice',
    ...             'filtfilt'), loc='best')
    >>> plt.grid(True)
    >>> plt.show()

    """
    xp = array_namespace(b, a, x, zi)

    b = np.atleast_1d(b)
    a = np.atleast_1d(a)
    x = np.asarray(x)
    if zi is not None:
       zi = np.asarray(zi)

    if not (b.ndim == 1 and xp_size(b) > 0):
        raise ValueError(f"Parameter b is not a non-empty 1d array, since {b.shape=}!")
    if not (a.ndim == 1 and xp_size(a) > 0):
        raise ValueError(f"Parameter a is not a non-empty 1d array, since {a.shape=}!")

    if len(a) == 1:
        # This path only supports types fdgFDGO to mirror _linear_filter below.
        # Any of b, a, x, or zi can set the dtype, but there is no default
        # casting of other types; instead a NotImplementedError is raised.
        b = np.asarray(b)
        a = np.asarray(a)
        x = _validate_x(x)
        inputs = [b, a, x]
        if zi is not None:
            # _linear_filter does not broadcast zi, but does do expansion of
            # singleton dims.
            zi = np.asarray(zi)
            if zi.ndim != x.ndim:
                raise ValueError("Dimensions of parameters x and zi must match, but " +
                                 f"{x.ndim=}, {zi.ndim=}!")
            expected_shape = list(x.shape)
            expected_shape[axis] = b.shape[0] - 1
            expected_shape = tuple(expected_shape)
            # check the trivial case where zi is the right shape first
            if zi.shape != expected_shape:
                strides = zi.ndim * [None]
                if axis < 0:
                    axis += zi.ndim
                for k in range(zi.ndim):
                    if k == axis and zi.shape[k] == expected_shape[k]:
                        strides[k] = zi.strides[k]
                    elif k != axis and zi.shape[k] == expected_shape[k]:
                        strides[k] = zi.strides[k]
                    elif k != axis and zi.shape[k] == 1:
                        strides[k] = 0
                    else:
                        raise ValueError('Unexpected shape for parameter zi: expected '
                                         f'{expected_shape}, found {zi.shape}.')
                zi = np.lib.stride_tricks.as_strided(zi, expected_shape,
                                                     strides)
            inputs.append(zi)
        dtype = np.result_type(*inputs)

        if dtype.char not in 'fdgFDGO':
            raise NotImplementedError("Parameter's dtypes produced result type " +
                                      f"'{dtype}', which is not supported!")

        b = np.array(b, dtype=dtype)
        a = np.asarray(a, dtype=dtype)
        b /= a[0]
        x = np.asarray(x, dtype=dtype)

        out_full = np.apply_along_axis(lambda y: np.convolve(b, y), axis, x)
        ind = out_full.ndim * [slice(None)]
        if zi is not None:
            ind[axis] = slice(zi.shape[axis])
            out_full[tuple(ind)] += zi

        ind[axis] = slice(out_full.shape[axis] - len(b) + 1)
        out = out_full[tuple(ind)]

        if zi is None:
            return xp.asarray(out)
        else:
            ind[axis] = slice(out_full.shape[axis] - len(b) + 1, None)
            zf = out_full[tuple(ind)]
            return xp.asarray(out), xp.asarray(zf)
    else:
        if zi is None:
            result =_sigtools._linear_filter(b, a, x, axis)
            return xp.asarray(result)
        else:
            out, zf = _sigtools._linear_filter(b, a, x, axis, zi)
            return xp.asarray(out), xp.asarray(zf)

