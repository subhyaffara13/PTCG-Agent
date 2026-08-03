import math


def _convert_to_2d(coo, axis):
    axis_coords = tuple(coo.coords[i] for i in axis)
    axis_shape = tuple(coo.shape[i] for i in axis)
    axis_ravel = _ravel_coords(axis_coords, axis_shape)

    ndim = len(coo.coords)
    non_axis = tuple(i for i in range(ndim) if i not in axis)
    if non_axis:
        non_axis_coords = tuple(coo.coords[i] for i in non_axis)
        non_axis_shape = tuple(coo.shape[i] for i in non_axis)
        non_axis_ravel = _ravel_coords(non_axis_coords, non_axis_shape)
        coords_2d = (non_axis_ravel, axis_ravel)
        shape_2d = (math.prod(non_axis_shape), math.prod(axis_shape))
    else:  # all axes included in axis so result will have 1 element
        coords_2d = (axis_ravel,)
        shape_2d = (math.prod(axis_shape),)
        non_axis_shape = ()

    new_coo = coo_array((coo.data, coords_2d), shape=shape_2d)
    return new_coo, non_axis_shape

