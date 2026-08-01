
def map_functionalize(ctx, f, xs, pos_args):
    from torch._higher_order_ops.utils import (
        _check_alias_and_mutation,
        first_slice_copy,
    )

    unwrapped_xs = ctx.unwrap_tensors(xs)
    unwrapped_args = ctx.unwrap_tensors(pos_args)
    wrapped_fn = ctx.functionalize(_maybe_run_with_interpreter(f))

    with ctx.redispatch_to_next():
        # Use first_slice_copy instead of _unstack_pytree to avoid
        # iterating over batch dim, which would guard on symbolic sizes.
        example_inputs = (
            *pytree.tree_map(first_slice_copy, unwrapped_xs),
            *unwrapped_args,
        )
        pre_dispatch = hasattr(ctx, "mode") and ctx.mode.pre_dispatch
        _check_alias_and_mutation(f, example_inputs, "map", pre_dispatch)
        map_return = map_impl(wrapped_fn, unwrapped_xs, unwrapped_args)
        return ctx.wrap_tensors(map_return)

