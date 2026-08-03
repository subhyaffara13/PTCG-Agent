import itertools

def associative_scan_functionalize(ctx, combine_fn, xs, additional_inputs):
    from torch._higher_order_ops.utils import _check_alias_and_mutation

    unwrapped_xs = ctx.unwrap_tensors(xs)
    unwrapped_additional_inputs = ctx.unwrap_tensors(additional_inputs)
    with ctx.redispatch_to_next():
        functional_combine_fn = ctx.functionalize(
            _maybe_run_with_interpreter(combine_fn)
        )
        pre_dispatch = hasattr(ctx, "mode") and ctx.mode.pre_dispatch
        sample_unwrapped_xs_sliced = [
            first_slice_copy(inp) for inp in itertools.chain(unwrapped_xs, unwrapped_xs)
        ]
        sample_inputs = list(
            itertools.chain(
                sample_unwrapped_xs_sliced,
                unwrapped_additional_inputs,
            )
        )
        _check_alias_and_mutation(
            combine_fn, sample_inputs, "associative_scan", pre_dispatch
        )
        ret = associative_scan_op(
            functional_combine_fn,
            unwrapped_xs,
            unwrapped_additional_inputs,
        )
    return ctx.wrap_tensors(ret)

