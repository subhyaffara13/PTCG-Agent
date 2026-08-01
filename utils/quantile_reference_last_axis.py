
def quantile_reference_last_axis(x, p, nan_policy, method):
    if nan_policy == 'omit':
        x = x[~np.isnan(x)]
    p_mask = np.isnan(p)
    p = p.copy()
    p[p_mask] = 0.5
    if method == 'harrell-davis':
        # hdquantiles returns masked element if length along axis is 1 (bug)
        res = (np.full_like(p, x[0]) if x.size == 1
               else stats.mstats.hdquantiles(x, p).data)
    elif method.startswith('round'):
        res = winsor_reference_1d(np.sort(x), p, method)
    else:
        res = np.quantile(x, p, method=method)

    res = np.asarray(res)
    if nan_policy == 'propagate' and np.any(np.isnan(x)):
        res[:] = np.nan

    res[p_mask] = np.nan
    return res

