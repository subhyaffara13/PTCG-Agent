
def symiirorder2(input, r, omega, precision=-1.0):
    """
    Implement a smoothing IIR filter with mirror-symmetric boundary conditions
    using a cascade of second-order sections.

    The second section uses a reversed sequence.  This implements the following
    transfer function::

                                  cs^2
         H(z) = ---------------------------------------
                (1 - a2/z - a3/z^2) (1 - a2 z - a3 z^2 )

    where::

          a2 = 2 * r * cos(omega)
          a3 = - r ** 2
          cs = 1 - 2 * r * cos(omega) + r ** 2

    Parameters
    ----------
    input : ndarray
        The input signal.
    r, omega : float
        Parameters in the transfer function.
    precision : float
        Specifies the precision for calculating initial conditions
        of the recursive filter based on mirror-symmetric input.

    Returns
    -------
    output : ndarray
        The filtered signal.
    """
    xp = array_namespace(input)
    input = xp_promote(input, force_floating=True, xp=xp)
    # This function uses C internals
    input = np.ascontiguousarray(input)

    if r >= 1.0:
        raise ValueError('r must be less than 1.0')

    if input.ndim > 2:
        raise ValueError('Input must be 1D or 2D')

    squeeze_dim = False
    if input.ndim == 1:
        input = input[None, :]
        squeeze_dim = True

    rsq = r * r
    a2 = 2 * r * math.cos(omega)
    a3 = -rsq
    cs = 1 - 2 * r * math.cos(omega) + rsq
    sos = np.asarray([cs, 0, 0, 1, -a2, -a3], dtype=input.dtype)

    # Find the starting (forward) conditions.
    ic_fwd = symiirorder2_ic_fwd(input, r, omega, precision)

    # Apply first the system cs / (1 - a2 * z^-1 - a3 * z^-2)
    # Compute the initial conditions in the form expected by sosfilt
    # coef = np.asarray([[a3, a2], [0, a3]], dtype=input.dtype)
    coef = np.asarray([[a3, a2], [0, a3]], dtype=input.dtype)
    zi = np.matmul(coef, ic_fwd[:, :, None])[:, :, 0]

    y_fwd, _ = sosfilt(sos, axis_slice(input, 2), zi=zi[None])
    y_fwd = np.c_[ic_fwd, y_fwd]

    # Then compute the symmetric backward starting conditions
    ic_bwd = symiirorder2_ic_bwd(input, r, omega, precision)

    # Apply the system cs / (1 - a2 * z^1 - a3 * z^2)
    # Compute the initial conditions in the form expected by sosfilt
    zi = np.matmul(coef, ic_bwd[:, :, None])[:, :, 0]
    y, _ = sosfilt(sos, axis_slice(y_fwd, -3, step=-1), zi=zi[None])
    out = np.c_[axis_reverse(y), axis_reverse(ic_bwd)]

    if squeeze_dim:
        out = out[0]

    return xp.asarray(out)

