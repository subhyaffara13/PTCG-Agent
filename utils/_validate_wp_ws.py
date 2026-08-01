
def _validate_wp_ws(wp, ws, fs, analog, *, xp):
    wp = xpx.atleast_nd(wp, ndim=1, xp=xp)
    ws = xpx.atleast_nd(ws, ndim=1, xp=xp)
    wp, ws = xp_promote(wp, ws, force_floating=True, xp=xp)

    if fs is not None:
        if analog:
            raise ValueError("fs cannot be specified for an analog filter")
        wp = 2 * wp / fs
        ws = 2 * ws / fs

    filter_type = 2 * (wp.shape[0] - 1) + 1
    if wp[0] >= ws[0]:
        filter_type += 1

    return wp, ws, filter_type

