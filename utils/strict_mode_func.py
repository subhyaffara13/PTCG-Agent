
def strict_mode_func(ctx, callable, inputs):
    unwrapped_inputs = ctx.unwrap_tensors(inputs)
    with ctx.redispatch_to_next():
        functional_callable = ctx.functionalize(callable)

        cond_return = strict_mode_op(functional_callable, unwrapped_inputs)
        return ctx.wrap_tensors(cond_return)

