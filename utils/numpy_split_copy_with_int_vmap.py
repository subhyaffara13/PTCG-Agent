
def numpy_split_copy_with_int_vmap(info, in_dims, x, splits, dim):
    x_bdim, _ , _ = in_dims
    x = x.movedim(x_bdim, 0)
    result, len_split = numpy_split_copy_with_int(x, splits, dim + 1)
    return (result, len_split), ([0 for _ in range(len(result))], None)

