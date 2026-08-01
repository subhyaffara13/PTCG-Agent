
def numpy_cube_setup_context(ctx, inputs, output):
    x, = inputs
    _cube, dx = output
    ctx.save_for_backward(x, dx)

