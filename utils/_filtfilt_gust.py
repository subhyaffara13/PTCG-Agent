
def _filtfilt_gust(b, a, x, axis=-1, irlen=None):
    """Forward-backward IIR filter that uses Gustafsson's method.

    Apply the IIR filter defined by ``(b,a)`` to `x` twice, first forward
    then backward, using Gustafsson's initial conditions [1]_.

    Let ``y_fb`` be the result of filtering first forward and then backward,
    and let ``y_bf`` be the result of filtering first backward then forward.
    Gustafsson's method is to compute initial conditions for the forward
    pass and the backward pass such that ``y_fb == y_bf``.

    Parameters
    ----------
    b : scalar or 1-D ndarray
        Numerator coefficients of the filter.
    a : scalar or 1-D ndarray
        Denominator coefficients of the filter.
    x : ndarray
        Data to be filtered.
    axis : int, optional
        Axis of `x` to be filtered.  Default is -1.
    irlen : int or None, optional
        The length of the nonnegligible part of the impulse response.
        If `irlen` is None, or if the length of the signal is less than
        ``2 * irlen``, then no part of the impulse response is ignored.

    Returns
    -------
    y : ndarray
        The filtered data.
    x0 : ndarray
        Initial condition for the forward filter.
    x1 : ndarray
        Initial condition for the backward filter.

    Notes
    -----
    Typically the return values `x0` and `x1` are not needed by the
    caller.  The intended use of these return values is in unit tests.

    References
    ----------
    .. [1] F. Gustaffson. Determining the initial states in forward-backward
           filtering. Transactions on Signal Processing, 46(4):988-992, 1996.

    """
    # In the comments, "Gustafsson's paper" and [1] refer to the
    # paper referenced in the docstring.

    b = np.atleast_1d(b)
    a = np.atleast_1d(a)

    order = max(len(b), len(a)) - 1
    if order == 0:
        # The filter is just scalar multiplication, with no state.
        scale = (b[0] / a[0])**2
        y = scale * x
        return y, np.array([]), np.array([])

    if axis != -1 or axis != x.ndim - 1:
        # Move the axis containing the data to the end.
        x = np.swapaxes(x, axis, x.ndim - 1)

    # n is the number of samples in the data to be filtered.
    n = x.shape[-1]

    if irlen is None or n <= 2*irlen:
        m = n
    else:
        m = irlen

    # Create Obs, the observability matrix (called O in the paper).
    # This matrix can be interpreted as the operator that propagates
    # an arbitrary initial state to the output, assuming the input is
    # zero.
    # In Gustafsson's paper, the forward and backward filters are not
    # necessarily the same, so he has both O_f and O_b.  We use the same
    # filter in both directions, so we only need O. The same comment
    # applies to S below.
    Obs = np.zeros((m, order))
    zi = np.zeros(order)
    zi[0] = 1
    Obs[:, 0] = lfilter(b, a, np.zeros(m), zi=zi)[0]
    for k in range(1, order):
        Obs[k:, k] = Obs[:-k, 0]

    # Obsr is O^R (Gustafsson's notation for row-reversed O)
    Obsr = Obs[::-1]

    # Create S.  S is the matrix that applies the filter to the reversed
    # propagated initial conditions.  That is,
    #     out = S.dot(zi)
    # is the same as
    #     tmp, _ = lfilter(b, a, zeros(), zi=zi)  # Propagate ICs.
    #     out = lfilter(b, a, tmp[::-1])          # Reverse and filter.

    # Equations (5) & (6) of [1]
    S = lfilter(b, a, Obs[::-1], axis=0)

    # Sr is S^R (row-reversed S)
    Sr = S[::-1]

    # M is [(S^R - O), (O^R - S)]
    if m == n:
        M = np.hstack((Sr - Obs, Obsr - S))
    else:
        # Matrix described in section IV of [1].
        M = np.zeros((2*m, 2*order))
        M[:m, :order] = Sr - Obs
        M[m:, order:] = Obsr - S

    # Naive forward-backward and backward-forward filters.
    # These have large transients because the filters use zero initial
    # conditions.
    y_f = lfilter(b, a, x)
    y_fb = lfilter(b, a, y_f[..., ::-1])[..., ::-1]

    y_b = lfilter(b, a, x[..., ::-1])[..., ::-1]
    y_bf = lfilter(b, a, y_b)

    delta_y_bf_fb = y_bf - y_fb
    if m == n:
        delta = delta_y_bf_fb
    else:
        start_m = delta_y_bf_fb[..., :m]
        end_m = delta_y_bf_fb[..., -m:]
        delta = np.concatenate((start_m, end_m), axis=-1)

    # ic_opt holds the "optimal" initial conditions.
    # The following code computes the result shown in the formula
    # of the paper between equations (6) and (7).
    if delta.ndim == 1:
        ic_opt = linalg.lstsq(M, delta)[0]
    else:
        # Reshape delta so it can be used as an array of multiple
        # right-hand-sides in linalg.lstsq.
        delta2d = delta.reshape(-1, delta.shape[-1]).T
        ic_opt0 = linalg.lstsq(M, delta2d)[0].T
        ic_opt = ic_opt0.reshape(delta.shape[:-1] + (M.shape[-1],))

    # Now compute the filtered signal using equation (7) of [1].
    # First, form [S^R, O^R] and call it W.
    if m == n:
        W = np.hstack((Sr, Obsr))
    else:
        W = np.zeros((2*m, 2*order))
        W[:m, :order] = Sr
        W[m:, order:] = Obsr

    # Equation (7) of [1] says
    #     Y_fb^opt = Y_fb^0 + W * [x_0^opt; x_{N-1}^opt]
    # `wic` is (almost) the product on the right.
    # W has shape (m, 2*order), and ic_opt has shape (..., 2*order),
    # so we can't use W.dot(ic_opt).  Instead, we dot ic_opt with W.T,
    # so wic has shape (..., m).
    wic = ic_opt.dot(W.T)

    # `wic` is "almost" the product of W and the optimal ICs in equation
    # (7)--if we're using a truncated impulse response (m < n), `wic`
    # contains only the adjustments required for the ends of the signal.
    # Here we form y_opt, taking this into account if necessary.
    y_opt = y_fb
    if m == n:
        y_opt += wic
    else:
        y_opt[..., :m] += wic[..., :m]
        y_opt[..., -m:] += wic[..., -m:]

    x0 = ic_opt[..., :order]
    x1 = ic_opt[..., -order:]
    if axis != -1 or axis != x.ndim - 1:
        # Restore the data axis to its original position.
        x0 = np.swapaxes(x0, axis, x.ndim - 1)
        x1 = np.swapaxes(x1, axis, x.ndim - 1)
        y_opt = np.swapaxes(y_opt, axis, x.ndim - 1)

    return y_opt, x0, x1

