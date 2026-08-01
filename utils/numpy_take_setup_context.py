
def numpy_take_setup_context(ctx, inputs, output):
    _x, ind, ind_inv, dim = inputs
    ctx.dim = dim
    ctx.save_for_backward(ind, ind_inv)

