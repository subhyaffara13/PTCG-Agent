
def numpy_split_copy_setup_context(ctx, inputs, output):
    _, _, dim = inputs
    ctx.dim = dim

