
def numpy_take_vmap(info, in_dims, x, ind, ind_inv, dim):
    x_bdim, ind_bdim, ind_inv_bdim, _ = in_dims

    # wrap dim
    logical_dim = x.dim() if x_bdim is None else x_bdim - 1
    dim = dim if dim >= 0 else dim + logical_dim

    def expand_bdim(x, x_bdim):
        if x_bdim is None:
            return x.expand(info.batch_size, *x.shape)
        return x.movedim(x_bdim, 0)

    x = expand_bdim(x, x_bdim)
    ind = expand_bdim(ind, ind_bdim)
    ind_inv = expand_bdim(ind_inv, ind_inv_bdim)

    return numpy_take(x, ind, ind_inv, dim + 1), 0

