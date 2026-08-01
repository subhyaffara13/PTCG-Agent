
def numpy_split_copy_vmap(info, in_dims, x, splits, dim):
    x_bdim, _ , _ = in_dims
    x = x.movedim(x_bdim, 0)
    result = numpy_split_copy(x, splits, dim + 1)
    return result, 0

