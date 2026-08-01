
def numpy_split_copy_with_int_backward(ctx, grad_out, _):
    return torch.ops._torch_testing.numpy_cat(grad_out, dim=ctx.dim), None, None

