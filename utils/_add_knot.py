
def _add_knot(x, t, k, residuals):
    """Insert a new knot given reduals."""
    fparts, ix = _split(x, t, k, residuals)

    # find the interval with max fparts and non-zero number of x values inside
    idx_max = -101
    fpart_max = -1e100
    for i in range(len(fparts)):
        if ix[i+1] - ix[i] > 1 and fparts[i] > fpart_max:
            idx_max = i
            fpart_max = fparts[i]

    if idx_max == -101:
        raise ValueError("Internal error, please report it to SciPy developers.")

    # round up, like Dierckx does? This is really arbitrary though.
    idx_newknot = (ix[idx_max] + ix[idx_max+1] + 1) // 2
    new_knot = x[idx_newknot]
    idx_t = np.searchsorted(t, new_knot)
    t_new = np.r_[t[:idx_t], new_knot, t[idx_t:]]
    return t_new

