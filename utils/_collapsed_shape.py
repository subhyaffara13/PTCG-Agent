
def _collapsed_shape(shape: ShapeType, start: int, end: int) -> tuple[int, ...]:
    """
    Returns the shape of a with dims in [start, end) merged into a single dimension.
    """
    # Special-case for zero dimensional tensors
    shape = (1,) if len(shape) == 0 else tuple(shape)

    dim_length = 1
    for s in shape[start : end + 1]:
        dim_length = dim_length * s

    return shape[0:start] + (dim_length,) + shape[end + 1 :]

