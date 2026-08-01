
def _process_axes(ndim_a, ndim_b, axes):
    if isinstance(axes, int):
        if axes < 1 or axes > min(ndim_a, ndim_b):
            raise ValueError("axes integer is out of bounds for input arrays")
        axes_a = list(range(ndim_a - axes, ndim_a))
        axes_b = list(range(axes))
    elif isinstance(axes, tuple | list):
        if len(axes) != 2:
            raise ValueError("axes must be a tuple/list of length 2")
        axes_a, axes_b = axes
        if len(axes_a) != len(axes_b):
            raise ValueError("axes lists/tuples must be of the same length")
        if any(ax >= ndim_a or ax < -ndim_a for ax in axes_a) or \
           any(bx >= ndim_b or bx < -ndim_b for bx in axes_b):
            raise ValueError("axes indices are out of bounds for input arrays")
    else:
        raise TypeError("axes must be an integer or a tuple/list of integers")

    axes_a = [axis + ndim_a if axis < 0 else axis for axis in axes_a]
    axes_b = [axis + ndim_b if axis < 0 else axis for axis in axes_b]
    return axes_a, axes_b

