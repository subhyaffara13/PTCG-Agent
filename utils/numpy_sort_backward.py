
def numpy_sort_backward(ctx, grad_out, grad_ind, grad_ind_inv):
    ind, ind_inv = ctx.saved_tensors
    return numpy_take(grad_out, ind_inv, ind, ctx.dim), None

