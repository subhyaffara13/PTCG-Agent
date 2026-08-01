
def _convolve_or_correlate(f, a, v, mode, propagate_mask):
    """
    Helper function for ma.correlate and ma.convolve
    """
    if propagate_mask:
        # results which are contributed to by either item in any pair being invalid
        mask = (
            f(getmaskarray(a), np.ones(np.shape(v), dtype=bool), mode=mode)
          | f(np.ones(np.shape(a), dtype=bool), getmaskarray(v), mode=mode)
        )
        data = f(getdata(a), getdata(v), mode=mode)
    else:
        # results which are not contributed to by any pair of valid elements
        mask = ~f(~getmaskarray(a), ~getmaskarray(v), mode=mode)
        data = f(filled(a, 0), filled(v, 0), mode=mode)

    return masked_array(data, mask=mask)

