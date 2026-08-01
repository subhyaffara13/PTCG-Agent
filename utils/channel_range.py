
def channel_range(input, axis=0):
    """Find the range of weights associated with a specific channel."""
    size_of_tensor_dim = input.ndim
    axis_list = list(range(size_of_tensor_dim))
    axis_list.remove(axis)

    mins = min_over_ndim(input, axis_list)
    maxs = max_over_ndim(input, axis_list)

    if mins.size(0) != input.size(axis):
        raise AssertionError(
            "Dimensions of resultant channel range does not match size of requested axis"
        )
    return maxs - mins

