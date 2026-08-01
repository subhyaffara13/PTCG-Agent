
def estimated_cdf_reference_last_axis(x, y, nan_policy, method):
    i_nan = np.isnan(x)
    if nan_policy == 'propagate' and np.any(i_nan):
        return np.full_like(y, np.nan)
    elif nan_policy == 'omit':
        x = x[~i_nan]
    return stats.estimated_cdf(x, y, keepdims=True, method=method)

