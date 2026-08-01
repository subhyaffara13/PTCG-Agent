
def symiirorder_nd(func, input, *args, axis=-1, **kwargs):
    axis = normalize_axis_index(axis, input.ndim)
    input_shape = input.shape
    input_ndim = input.ndim
    if input.ndim > 1:
        input, input_shape = collapse_2d(input, axis)

    out = func(input, *args, **kwargs)

    if input_ndim > 1:
        out = out.reshape(input_shape)
        out = moveaxis(out, -1, axis)
        if not out.flags.c_contiguous:
            out = out.copy()
    return out

