
def numpy_mul_backward(ctx, grad_out):
    x, y = ctx.saved_tensors
    grad_x = grad_out * y if ctx.needs_input_grad[0] else None
    grad_y = grad_out * x if ctx.needs_input_grad[1] else None
    return grad_x, grad_y

