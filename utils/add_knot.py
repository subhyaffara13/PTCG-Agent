
def add_knot(x, t, k, residuals):
    """Add a new knot.

    (Approximately) replicate FITPACK's logic:
      1. split the `x` array into knot intervals, ``t(j+k) <= x(i) <= t(j+k+1)``
      2. find the interval with the maximum sum of residuals
      3. insert a new knot into the middle of that interval.

    NB: a new knot is in fact an `x` value at the middle of the interval.
    So *the knots are a subset of `x`*.

    This routine is an analog of
    https://github.com/scipy/scipy/blob/v1.11.4/scipy/interpolate/fitpack/fpcurf.f#L190-L215
    (cf _split function)

    and https://github.com/scipy/scipy/blob/v1.11.4/scipy/interpolate/fitpack/fpknot.f
    """
    new_knot = _dierckx.fpknot(x, t, k, residuals)

    idx_t = np.searchsorted(t, new_knot)
    t_new = np.r_[t[:idx_t], new_knot, t[idx_t:]]
    return t_new

