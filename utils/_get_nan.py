
def _get_nan(*data, shape=(), xp=None):
    xp = array_namespace(*data) if xp is None else xp
    # Get NaN of appropriate dtype for data
    dtype = xp_result_type(*data, force_floating=True, xp=xp)
    device = xp_result_device(*data)
    res = xp.full(shape, xp.nan, dtype=dtype, device=device)
    if not shape:
        res = res[()]
    # whenever mdhaber/marray#89 is resolved, could just return `res`
    return res.data if is_marray(xp) else res

