
def numpy_split_copy_with_int_setup_context(ctx, inputs, output):
    _, _, dim = inputs
    ctx.dim = dim

