
def scan_functionalize(ctx, combine_fn, init, xs, additional_inputs):
    from torch._higher_order_ops.utils import (
        _check_alias_and_mutation,
        _maybe_run_with_interpreter,
    )

    unwrapped_xs = ctx.unwrap_tensors(xs)
    unwrapped_init = ctx.unwrap_tensors(init)
    unwrapped_additional_inputs = ctx.unwrap_tensors(additional_inputs)

    with ctx.redispatch_to_next():
        functional_combine_fn = ctx.functionalize(
            _maybe_run_with_interpreter(combine_fn)
        )
        sample_unwrapped_xs_sliced = [first_slice_copy(inp) for inp in unwrapped_xs]
        sample_inputs = list(
            itertools.chain(
                unwrapped_init,
                sample_unwrapped_xs_sliced,
                unwrapped_additional_inputs,
            )
        )
        pre_dispatch = hasattr(ctx, "mode") and ctx.mode.pre_dispatch
        _check_alias_and_mutation(combine_fn, sample_inputs, "scan", pre_dispatch)
        ret = scan_op(
            functional_combine_fn,
            unwrapped_init,
            unwrapped_xs,
            unwrapped_additional_inputs,
        )
    return ctx.wrap_tensors(ret)

