
def numpy_sort_vmap(info, in_dims, x, dim):
    x_bdim, _ = in_dims
    x = x.movedim(x_bdim, 0)
    dim = dim if dim >= 0 else dim + x.dim() - 1
    result = numpy_sort(x, dim + 1)
    return result, (0, 0, 0)

