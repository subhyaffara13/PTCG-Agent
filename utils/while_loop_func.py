
def while_loop_func(
    ctx, cond_fn, body_fn, carried_inputs, additional_inputs, stack_output=False
):
    from torch._higher_order_ops.utils import _check_alias_and_mutation

    op = while_loop_stack_output_op if stack_output else while_loop_op

    unwrapped_carried_inputs = ctx.unwrap_tensors(carried_inputs)
    unwrapped_additional_inputs = ctx.unwrap_tensors(additional_inputs)
    unwrapped_inputs = unwrapped_carried_inputs + unwrapped_additional_inputs
    with ctx.redispatch_to_next():
        functional_cond_fn = ctx.functionalize(_maybe_run_with_interpreter(cond_fn))
        functional_body_fn = ctx.functionalize(_maybe_run_with_interpreter(body_fn))
        pre_dispatch = hasattr(ctx, "mode") and ctx.mode.pre_dispatch
        for fn, fn_name in [
            (cond_fn, "cond_fn"),
            (body_fn, "body_fn"),
        ]:
            _check_alias_and_mutation(fn, unwrapped_inputs, fn_name, pre_dispatch)
        ret = op(
            functional_cond_fn,
            functional_body_fn,
            unwrapped_carried_inputs,
            unwrapped_additional_inputs,
        )
        return ctx.wrap_tensors(ret)

