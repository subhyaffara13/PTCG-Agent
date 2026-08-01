
def numpy_cube_backward(ctx, grad_out, grad_dx):
    x, dx = ctx.saved_tensors
    grad_x = numpy_mul(grad_out, dx) + 6 * numpy_mul(grad_dx, x)
    return grad_x

