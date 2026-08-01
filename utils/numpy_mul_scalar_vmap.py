
def numpy_mul_scalar_vmap(info, in_dims, x, *, scalar):
    x_bdim, = in_dims
    x = x.movedim(x_bdim, -1) if x_bdim is not None else x.unsqueeze(-1)
    result = x * scalar
    result = result.movedim(-1, 0)
    return result, 0

