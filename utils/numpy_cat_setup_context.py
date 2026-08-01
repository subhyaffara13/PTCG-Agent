
def numpy_cat_setup_context(ctx, inputs, output):
    xs, dim = inputs
    ctx.dim_sizes = [x.shape[dim] for x in xs]
    ctx.dim = dim

