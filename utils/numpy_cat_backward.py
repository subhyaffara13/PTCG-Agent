
def numpy_cat_backward(ctx, grad_out):
    dim_sizes = ctx.dim_sizes
    dim = ctx.dim

    splits = list(np.cumsum(dim_sizes)[:-1])
    grad_xs = torch.ops._torch_testing.numpy_split_copy(grad_out, splits, dim)
    return grad_xs, None

