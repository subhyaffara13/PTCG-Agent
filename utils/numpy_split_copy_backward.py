
def numpy_split_copy_backward(ctx, grad_out):
    result = torch.ops._torch_testing.numpy_cat(grad_out, dim=ctx.dim)
    return result, None, None

