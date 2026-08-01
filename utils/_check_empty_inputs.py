
def _check_empty_inputs(samples, axis, xp=None):
    """
    Check for empty sample; return appropriate output for a vectorized hypotest
    """
    xp = array_namespace(*samples) if xp is None else xp
    # if none of the samples are empty, we need to perform the test
    if not any(xp_size(sample) == 0 for sample in samples):
        return None
    # otherwise, the statistic and p-value will be either empty arrays or
    # arrays with NaNs. Produce the appropriate array and return it.
    output_shape = _broadcast_array_shapes_remove_axis(samples, axis)
    NaN = _get_nan(*samples)
    output = xp.full(output_shape, xp.nan, dtype=NaN.dtype)
    return output

