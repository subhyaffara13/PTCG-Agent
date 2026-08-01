
def symiirorder1(signal, c0, z1, precision=-1.0):
    """
    Implement a smoothing IIR filter with mirror-symmetric boundary conditions
    using a cascade of first-order sections.

    The second section uses a reversed sequence.  This implements a system with
    the following transfer function and mirror-symmetric boundary conditions::

                           c0
           H(z) = ---------------------
                   (1-z1/z) (1 - z1 z)

    The resulting signal will have mirror symmetric boundary conditions
    as well.

    Parameters
    ----------
    signal : ndarray
        The input signal. If 2D, then the filter will be applied in a batched
        fashion across the last axis.
    c0, z1 : scalar
        Parameters in the transfer function.
    precision : float, optional
        Specifies the precision for calculating initial conditions
        of the recursive filter based on mirror-symmetric input.

    Returns
    -------
    output : ndarray
        The filtered signal.
    """
    xp = array_namespace(signal)
    signal = xp_promote(signal, force_floating=True, xp=xp)
    # This function uses C internals
    signal = np.asarray(signal)

    if abs(z1) >= 1:
        raise ValueError('|z1| must be less than 1.0')

    if signal.ndim > 2:
        raise ValueError('Input must be 1D or 2D')

    squeeze_dim = False
    if signal.ndim == 1:
        signal = signal[None, :]
        squeeze_dim = True

    y0 = symiirorder1_ic(signal, z1, precision)

    # Apply first the system 1 / (1 - z1 * z^-1)
    b = np.ones(1, dtype=signal.dtype)
    a = np.r_[1, -z1]
    a = a.astype(signal.dtype)

    # Compute the initial state for lfilter.
    zii = y0 * z1

    y1, _ = lfilter(b, a, axis_slice(signal, 1), zi=zii)
    y1 = np.c_[y0, y1]

    # Compute backward symmetric condition and apply the system
    # c0 / (1 - z1 * z)
    b = np.asarray([c0], dtype=signal.dtype)
    out_last = -c0 / (z1 - 1.0) * axis_slice(y1, -1)

    # Compute the initial state for lfilter.
    zii = out_last * z1

    # Apply the system c0 / (1 - z1 * z) by reversing the output of the previous stage
    out, _ = lfilter(b, a, axis_slice(y1, -2, step=-1), zi=zii)
    out = np.c_[axis_reverse(out), out_last]

    if squeeze_dim:
        out = out[0]

    return xp.asarray(out)

