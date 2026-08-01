
def _nanmedian1d(arr1d, overwrite_input=False):
    """
    Private function for rank 1 arrays. Compute the median ignoring NaNs.
    See nanmedian for parameter usage
    """
    arr1d_parsed, _, overwrite_input = _remove_nan_1d(
        arr1d, overwrite_input=overwrite_input,
    )

    if arr1d_parsed.size == 0:
        # Ensure that a nan-esque scalar of the appropriate type (and unit)
        # is returned for `timedelta64` and `complexfloating`
        return arr1d[-1]

    return np.median(arr1d_parsed, overwrite_input=overwrite_input)

