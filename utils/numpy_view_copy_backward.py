
def numpy_view_copy_backward(ctx, grad_out):
    return torch.ops._torch_testing.numpy_view_copy(grad_out, ctx.x_shape), None

