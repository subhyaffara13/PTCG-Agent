
def lfilter_zi(b, a):
    r"""Construct initial conditions for `lfilter` for step response steady-state.

    Compute an initial state `zi` for the `lfilter` function that corresponds
    to the steady state of the step response.

    A typical use of this function is to set the initial state so that the
    output of the filter starts at the same value as the first element of
    the signal to be filtered.

    Parameters
    ----------
    b : array_like
        The numerator coefficient vector as a 1-D sequence.
    a : array_like
        The denominator coefficient vector as a 1-D sequence.  If ``a[0]``
        is not 1, then both `a` and `b` are normalized by ``a[0]``.
        Hence, ``a[0] != 0`` must hold.

    Returns
    -------
    zi : 1-D ndarray
        The initial state for the filter.

    Raises
    ------
    ValueError
        If ``a[0] == 0`` (invalid denominator polynomial) or
        ``sum(a) == 0`` (unstable filter).

    See Also
    --------
    lfilter, lfiltic, filtfilt

    Notes
    -----
    The parameters `b` and `a` represent a transfer function :math:`H(z) = Y(z)/X(z)`
    which is defined in the :ref:`tutorial_signal_TransferFunctionRepresentation`
    section of the :ref:`user_guide`. As discussed in [1]_, the final value of
    filtering a step response :math:`X(z) = z / (z-1)`, i.e., steady state, is given by

    .. math::

        y_\infty := \lim_{k\to\infty} y[k]
                  =  \lim_{z\to 1}\ (z-1)\, Y(z)
                  = \frac{\sum_{i=0}^M b_i}{\sum_{j=0}^N a_j} \,.

    If the denominator is zero, :math:`H(z)` has a pole at :math:`z_\infty=1`, which
    makes the filter unstable. For the transposed Direct Form II, which is implemented
    in `lfilter`, the initialization values :math:`z_k` for :math:`H(z)` can be
    determined by the recurrence equation

    .. math::

        z_k = z_{k+1} + x[0] \big( b_k - y_\infty a_k \big) \,,

    with :math:`x[0]` being the height of the input step function. Note that
    :math:`a_0=1` is assumed here, which is incorporated into this function by
    performing a normalization step.

    Examples
    --------
    The following code creates a lowpass Butterworth filter to filter a signal made up
    of ones. As expected of a lowpass filter, the output is also all ones. If the `zi`
    argument of `lfilter` had not been given, a transient signal would have been
    produced. The second signal illustrates that using the parameter `zi` supresses
    transients at the beginning of the output signal:

    >>> import numpy as np
    >>> from scipy.signal import lfilter, lfilter_zi, butter
    ...
    >>> b, a = butter(5, 0.25)
    >>> zi = lfilter_zi(b, a)
    >>> y0, zi0 = lfilter(b, a, np.ones(10), zi=zi)
    >>> y0
    array([1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.])
    >>> # Another signal:
    >>> x = np.array([0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0])
    >>> y1, zi1 = lfilter(b, a, x, zi=zi*x[0])
    >>> y1
    array([ 0.5       ,  0.5       ,  0.5       ,  0.49836039,  0.48610528,
        0.44399389,  0.35505241])

    Note that the `zi` argument to `lfilter` is computed using `lfilter_zi` and scaled
    by ``x[0]``. As a result, the output `y1` has no transient until the input drops
    from 0.5 to 0.

    References
    ----------
    .. [1] Boris Likhterov and Norman Kopeika. "Hardware-efficient technique for
           minimizing startup transients in Direct Form II digital filters". In:
           International Journal of Electronics -- Volume 90(7), July 2003, pp.
           471--479. :doi:`10.1080/00207210310001612482`
    """
    xp = array_namespace(b, a)

    # Note: As an alternative to this function, using `lfiltic` might work as well.
    # For example, when b,a = butter(N,Wn), then
    #    lfiltic(b, a, y=numpy.ones_like(a)*y_inf, x=numpy.ones_like(b)).
    # should produce the same result. Though, no obvious algorithmic advantages over
    # this implementation could be identified.

    # We could use scipy.signal.normalize, but it uses warnings in
    # cases where a ValueError is more appropriate, and it allows
    # b to be 2D.
    b, a = xp_promote(b, a, xp=xp, force_floating=True)  # need floats for division
    b = xpx.atleast_nd(b, ndim=1, xp=xp)
    a = xpx.atleast_nd(a, ndim=1, xp=xp)

    if not (b.ndim == a.ndim == 1):
        raise ValueError("Numerator `b` and Denominator `a` must be 1-D arrays, " +
                         f"but {b.shape = }, {a.shape = }!")

    if a[0] == 0:
        raise ValueError("First coefficient of parameter `a` must be non-zero!")

    if a[0] != 1:  # Normalize the coefficients so a[0] == 1:
        b, a = b / a[0], a / a[0]

    if (sum_a := xp.sum(a)) == 0:
        raise ValueError("Filter not stable due to sum(a) == 0, i.e., " +
                         "having a pole at z = 1!")

    y_inf = xp.sum(b) / sum_a  # y[k → ∞] for unit-step input

    # Calculate `zi[k] = zi[k+1] + b - y_inf*a` allowing different length for a, b:
    n_a, n_b = a.shape[0], b.shape[0]
    n = max(n_a, n_b)
    b = xpx.pad(b, (0, n-n_b))
    a = xpx.pad(a, (0, n-n_a))
    # `xp.cumulative_sum((b - y_inf*a)[::-1])[-2::-1]` does not work in torch due to
    # unsupported slicing with a negative step index. Hence, `flip` is used:
    return xp.flip(xp.cumulative_sum(xp.flip(b - y_inf*a)))[1:]

