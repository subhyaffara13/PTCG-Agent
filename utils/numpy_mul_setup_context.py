
def numpy_mul_setup_context(ctx, inputs, output):
    ctx.save_for_backward(*inputs)

