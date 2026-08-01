
def numpy_mul_scalar_backward(ctx, grad_out):
    grad_x = grad_out * ctx.scalar
    return grad_x

