
def _mad_1d(x, center, nan_policy):
    # Median absolute deviation for 1-d array x.
    # This is a helper function for `median_abs_deviation`; it assumes its
    # arguments have been validated already.  In particular,  x must be a
    # 1-d numpy array, center must be callable, and if nan_policy is not
    # 'propagate', it is assumed to be 'omit', because 'raise' is handled
    # in `median_abs_deviation`.
    # No warning is generated if x is empty or all nan.
    isnan = np.isnan(x)
    if isnan.any():
        if nan_policy == 'propagate':
            return np.nan
        x = x[~isnan]
    if x.size == 0:
        # MAD of an empty array is nan.
        return np.nan
    # Edge cases have been handled, so do the basic MAD calculation.
    med = center(x)
    mad = np.median(np.abs(x - med))
    return mad

