
def numpy_cat_vmap(info, in_dims, x, dim):
    x_bdim, = in_dims
    result = numpy_cat(x, dim)
    return result, x_bdim

