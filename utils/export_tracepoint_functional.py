
def export_tracepoint_functional(ctx, *args, **kwargs):
    unwrapped_args = ctx.unwrap_tensors(args)
    unwrapped_kwargs = ctx.unwrap_tensors(kwargs)

    with ctx.redispatch_to_next():
        _export_tracepoint(*unwrapped_args, **unwrapped_kwargs)
        return args

