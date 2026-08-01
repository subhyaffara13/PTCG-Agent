
def _expand_mode(ndim_image, axes, mode):
    num_axes = len(axes)
    if not isinstance(mode, str) and isinstance(mode, Iterable):
        # set mode = 'constant' for any axes not being filtered
        modes = _ni_support._normalize_sequence(mode, num_axes)
        modes_temp = ['constant'] * ndim_image
        for m, ax in zip(modes, axes):
            modes_temp[ax] = m
        mode = modes_temp
    return mode

