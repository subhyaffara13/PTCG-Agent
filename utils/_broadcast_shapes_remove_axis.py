
def _broadcast_shapes_remove_axis(shapes, axis=None):
    """
    Broadcast shapes, dropping specified axes

    Same as _broadcast_array_shapes_remove_axis, but given a sequence
    of array shapes `shapes` instead of the arrays themselves.
    """
    shapes = _broadcast_shapes(shapes, axis)
    shape = shapes[0]
    if axis is not None:
        shape = np.delete(shape, axis)
    return tuple(shape)

