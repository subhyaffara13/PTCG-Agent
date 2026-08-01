
def inductor_compiled_code_functionalize(ctx, func, inputs, *, name=None):
    # Unwrap the functional tensors to get the underlying tensors
    unwrapped_inputs = ctx.unwrap_tensors(inputs)

    # Redispatch to the next handler in the dispatch chain
    with ctx.redispatch_to_next():
        kwargs = {"name": name} if name is not None else {}
        result = inductor_compiled_code(func, unwrapped_inputs, **kwargs)
        return ctx.wrap_tensors(result)

