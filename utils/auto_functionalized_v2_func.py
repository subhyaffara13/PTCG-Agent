
def auto_functionalized_v2_func(ctx, _mutable_op, **kwargs):
    unwrapped_kwargs = ctx.unwrap_tensors(kwargs)
    with ctx.redispatch_to_next():
        result = auto_functionalized_v2(_mutable_op, **unwrapped_kwargs)
    return ctx.wrap_tensors(result)

