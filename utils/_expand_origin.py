
def _expand_origin(ndim_image, axes, origin):
    num_axes = len(axes)
    origins = _ni_support._normalize_sequence(origin, num_axes)
    if num_axes < ndim_image:
        # set origin = 0 for any axes not being filtered
        origins_temp = [0,] * ndim_image
        for o, ax in zip(origins, axes):
            origins_temp[ax] = o
        origins = origins_temp
    return origins

