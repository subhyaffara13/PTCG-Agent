
def normalize_axis_index(ax, ndim, argname=None):
    if not (-ndim <= ax < ndim):
        raise AxisError(f"axis {ax} is out of bounds for array of dimension {ndim}")
    if ax < 0:
        ax += ndim
    return ax


def normalize_axis_index(axis, ndim):
    # Check if `axis` is in the correct range and normalize it
    if axis < -ndim or axis >= ndim:
        msg = f"axis {axis} is out of bounds for array of dimension {ndim}"
        raise AxisError(msg)

    if axis < 0:
        axis = axis + ndim
    return axis

