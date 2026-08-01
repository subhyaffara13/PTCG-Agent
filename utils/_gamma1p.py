
def _gamma1p(vals):
    """
    returns gamma(n+1), though with NaN at -1 instead of inf, c.f. #21827
    """
    res = gamma(vals + 1)
    # replace infinities at -1 (from gamma function at 0) with nan
    # gamma only returns inf for real inputs; can ignore complex case
    if isinstance(res, np.ndarray):
        if not _is_subdtype(vals.dtype, "c"):
            res[vals == -1] = np.nan
    elif np.isinf(res) and vals == -1:
        res = np.float64("nan")
    return res

