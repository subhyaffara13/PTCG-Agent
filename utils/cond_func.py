
def cond_func(ctx, pred, true_fn, false_fn, inputs):
    from torch._higher_order_ops.auto_functionalize import (
        can_auto_functionalize,
        do_auto_functionalize_v2,
    )
    from torch._higher_order_ops.utils import _check_alias_and_mutation, HopInstance

    hop_instance = HopInstance.create(cond_op, pred, true_fn, false_fn, inputs)
    # For now, we only support auto-functionalization for cond when using python
    # functionalization mode
    if can_auto_functionalize(hop_instance) and hasattr(ctx, "mode"):
        return do_auto_functionalize_v2(
            ctx.mode,
            hop_instance,
            tuple(pytree.tree_flatten((pred, true_fn, false_fn, inputs))[0]),
            {},
        )

    unwrapped_inputs = ctx.unwrap_tensors(inputs)
    unwrapped_pred = ctx.unwrap_tensors(pred)
    with ctx.redispatch_to_next():
        functional_true = ctx.functionalize(_maybe_run_with_interpreter(true_fn))
        functional_false = ctx.functionalize(_maybe_run_with_interpreter(false_fn))
        pre_dispatch = hasattr(ctx, "mode") and ctx.mode.pre_dispatch
        for branch, branch_name in [(true_fn, "cond_true"), (false_fn, "cond_false")]:
            _check_alias_and_mutation(
                branch, unwrapped_inputs, branch_name, pre_dispatch
            )

        cond_return = cond_op(
            unwrapped_pred, functional_true, functional_false, unwrapped_inputs
        )
        return ctx.wrap_tensors(cond_return)

