
def _set_wrap_both(padded, axis, width_pair, original_period):
    """
    Pad `axis` of `arr` with wrapped values.

    Parameters
    ----------
    padded : ndarray
        Input array of arbitrary shape.
    axis : int
        Axis along which to pad `arr`.
    width_pair : (int, int)
        Pair of widths that mark the pad area on both sides in the given
        dimension.
    original_period : int
        Original length of data on `axis` of `arr`.

    Returns
    -------
    pad_amt : tuple of ints, length 2
        New index positions of padding to do along the `axis`. If these are
        both 0, padding is done in this dimension.
    """
    left_pad, right_pad = width_pair
    period = padded.shape[axis] - right_pad - left_pad
    # Avoid wrapping with only a subset of the original area by ensuring period
    # can only be a multiple of the original area's length.
    period = period // original_period * original_period

    # If the current dimension of `arr` doesn't contain enough valid values
    # (not part of the undefined pad area) we need to pad multiple times.
    # Each time the pad area shrinks on both sides which is communicated with
    # these variables.
    new_left_pad = 0
    new_right_pad = 0

    if left_pad > 0:
        # Pad with wrapped values on left side
        # First slice chunk from left side of the non-pad area.
        # Use min(period, left_pad) to ensure that chunk is not larger than
        # pad area.
        slice_end = left_pad + period
        slice_start = slice_end - min(period, left_pad)
        right_slice = _slice_at_axis(slice(slice_start, slice_end), axis)
        right_chunk = padded[right_slice]

        if left_pad > period:
            # Chunk is smaller than pad area
            pad_area = _slice_at_axis(slice(left_pad - period, left_pad), axis)
            new_left_pad = left_pad - period
        else:
            # Chunk matches pad area
            pad_area = _slice_at_axis(slice(None, left_pad), axis)
        padded[pad_area] = right_chunk

    if right_pad > 0:
        # Pad with wrapped values on right side
        # First slice chunk from right side of the non-pad area.
        # Use min(period, right_pad) to ensure that chunk is not larger than
        # pad area.
        slice_start = -right_pad - period
        slice_end = slice_start + min(period, right_pad)
        left_slice = _slice_at_axis(slice(slice_start, slice_end), axis)
        left_chunk = padded[left_slice]

        if right_pad > period:
            # Chunk is smaller than pad area
            pad_area = _slice_at_axis(
                slice(-right_pad, -right_pad + period), axis)
            new_right_pad = right_pad - period
        else:
            # Chunk matches pad area
            pad_area = _slice_at_axis(slice(-right_pad, None), axis)
        padded[pad_area] = left_chunk

    return new_left_pad, new_right_pad

