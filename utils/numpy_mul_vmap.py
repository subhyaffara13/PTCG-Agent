
def numpy_mul_vmap(info, in_dims, x, y):
    x_bdim, y_bdim = in_dims
    x = x.movedim(x_bdim, -1) if x_bdim is not None else x.unsqueeze(-1)
    y = y.movedim(y_bdim, -1) if y_bdim is not None else y.unsqueeze(-1)
    result = x * y
    result = result.movedim(-1, 0)
    return result, 0

