
def numpy_view_copy_vmap(info, in_dims, x, shape):
    x_bdim, _ = in_dims
    x = x.movedim(x_bdim, 0)
    x_shape = x.shape[0]
    batch_shape = (x_shape, *shape)
    result = numpy_view_copy(x, batch_shape)
    return result, 0

