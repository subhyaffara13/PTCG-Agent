
def filtfilt_gust_opt(b, a, x):
    """
    An alternative implementation of filtfilt with Gustafsson edges.

    This function computes the same result as
    `scipy.signal._signaltools._filtfilt_gust`, but only 1-d arrays
    are accepted.  The problem is solved using `fmin` from `scipy.optimize`.
    `_filtfilt_gust` is significantly faster than this implementation.
    """
    def filtfilt_gust_opt_func(ics, b, a, x):
        """Objective function used in filtfilt_gust_opt."""
        m = max(len(a), len(b)) - 1
        z0f = ics[:m]
        z0b = ics[m:]
        y_f = lfilter(b, a, x, zi=z0f)[0]
        y_fb = lfilter(b, a, y_f[::-1], zi=z0b)[0][::-1]

        y_b = lfilter(b, a, x[::-1], zi=z0b)[0][::-1]
        y_bf = lfilter(b, a, y_b, zi=z0f)[0]
        value = np.sum((y_fb - y_bf)**2)
        return value

    m = max(len(a), len(b)) - 1
    zi = lfilter_zi(b, a)
    ics = np.concatenate((x[:m].mean()*zi, x[-m:].mean()*zi))
    result = fmin(filtfilt_gust_opt_func, ics, args=(b, a, x),
                  xtol=1e-10, ftol=1e-12,
                  maxfun=10000, maxiter=10000,
                  full_output=True, disp=False)
    opt, fopt, niter, funcalls, warnflag = result
    if warnflag > 0:
        raise RuntimeError(
            f"minimization failed in filtfilt_gust_opt: warnflag={warnflag}"
        )
    z0f = opt[:m]
    z0b = opt[m:]

    # Apply the forward-backward filter using the computed initial
    # conditions.
    y_b = lfilter(b, a, x[::-1], zi=z0b)[0][::-1]
    y = lfilter(b, a, y_b, zi=z0f)[0]

    return y, z0f, z0b

