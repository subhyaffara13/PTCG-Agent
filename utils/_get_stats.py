
def _get_stats(padded, axis, width_pair, length_pair, stat_func):
    """
    Calculate statistic for the empty-padded array in given dimension.

    Parameters
    ----------
    padded : ndarray
        Empty-padded array.
    axis : int
        Dimension in which the statistic is calculated.
    width_pair : (int, int)
        Pair of widths that mark the pad area on both sides in the given
        dimension.
    length_pair : 2-element sequence of None or int
        Gives the number of values in valid area from each side that is
        taken into account when calculating the statistic. If None the entire
        valid area in `padded` is considered.
    stat_func : function
        Function to compute statistic. The expected signature is
        ``stat_func(x: ndarray, axis: int, keepdims: bool) -> ndarray``.

    Returns
    -------
    left_stat, right_stat : ndarray
        Calculated statistic for both sides of `padded`.
    """
    # Calculate indices of the edges of the area with original values
    left_index = width_pair[0]
    right_index = padded.shape[axis] - width_pair[1]
    # as well as its length
    max_length = right_index - left_index

    # Limit stat_lengths to max_length
    left_length, right_length = length_pair
    if left_length is None or max_length < left_length:
        left_length = max_length
    if right_length is None or max_length < right_length:
        right_length = max_length

    if (left_length == 0 or right_length == 0) \
            and stat_func in {np.amax, np.amin}:
        # amax and amin can't operate on an empty array,
        # raise a more descriptive warning here instead of the default one
        raise ValueError("stat_length of 0 yields no value for padding")

    # Calculate statistic for the left side
    left_slice = _slice_at_axis(
        slice(left_index, left_index + left_length), axis)
    left_chunk = padded[left_slice]
    left_stat = stat_func(left_chunk, axis=axis, keepdims=True)
    _round_if_needed(left_stat, padded.dtype)

    if left_length == right_length == max_length:
        # return early as right_stat must be identical to left_stat
        return left_stat, left_stat

    # Calculate statistic for the right side
    right_slice = _slice_at_axis(
        slice(right_index - right_length, right_index), axis)
    right_chunk = padded[right_slice]
    right_stat = stat_func(right_chunk, axis=axis, keepdims=True)
    _round_if_needed(right_stat, padded.dtype)

    return left_stat, right_stat

