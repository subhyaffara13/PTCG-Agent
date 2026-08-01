
def _trace_wrapped_functionalized(ctx: Any, *args: Any, **kwargs: Any) -> Any:
    unwrapped_args = ctx.unwrap_tensors(args)
    with ctx.redispatch_to_next():
        return ctx.wrap_tensors(_trace_wrapped_op(*unwrapped_args, **kwargs))

