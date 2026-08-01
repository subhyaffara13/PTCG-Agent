
def collapse_2d(x, axis):
    x = moveaxis(x, axis, -1)
    x_shape = x.shape
    x = x.reshape(-1, x.shape[-1])
    if not x.flags.c_contiguous:
        x = x.copy()
    return x, x_shape

