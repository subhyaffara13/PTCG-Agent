
def normalize_axis(axis: int, rank: int) -> tuple[bool, int]:
    """
    Helper function that tries to return a normalized axis in the range [0, rank - 1].
    :parameter axis: The axis to normalize.
    :parameter rank: The tensor rank (number of dimensions).
    :return (is_valid, axis_norm)
    """
    axis_norm = axis + rank if axis < 0 else axis
    is_valid = axis_norm >= 0 and axis_norm < rank
    return is_valid, axis_norm

