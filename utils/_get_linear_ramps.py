
def _get_linear_ramps(padded, axis, width_pair, end_value_pair):
    """
    Construct linear ramps for empty-padded array in given dimension.

    Parameters
    ----------
    padded : ndarray
        Empty-padded array.
    axis : int
        Dimension in which the ramps are constructed.
    width_pair : (int, int)
        Pair of widths that mark the pad area on both sides in the given
        dimension.
    end_value_pair : (scalar, scalar)
        End values for the linear ramps which form the edge of the fully padded
        array. These values are included in the linear ramps.

    Returns
    -------
    left_ramp, right_ramp : ndarray
        Linear ramps to set on both sides of `padded`.
    """
    edge_pair = _get_edges(padded, axis, width_pair)

    left_ramp, right_ramp = (
        np.linspace(
            start=end_value,
            stop=edge.squeeze(axis),  # Dimension is replaced by linspace
            num=width,
            endpoint=False,
            dtype=padded.dtype,
            axis=axis
        )
        for end_value, edge, width in zip(
            end_value_pair, edge_pair, width_pair
        )
    )

    # Reverse linear space in appropriate dimension
    right_ramp = right_ramp[_slice_at_axis(slice(None, None, -1), axis)]

    return left_ramp, right_ramp

