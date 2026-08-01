
def invoke_leaf_function_functionalization(ctx, *all_args, **kwargs):
    from torch._higher_order_ops.auto_functionalize import (
        can_auto_functionalize,
        do_auto_functionalize_v2,
    )
    from torch._higher_order_ops.utils import HopInstance

    unwrapped_args = ctx.unwrap_tensors(all_args)
    hop_instance = HopInstance.create(invoke_leaf_function, *unwrapped_args, **kwargs)
    if can_auto_functionalize(hop_instance):
        return do_auto_functionalize_v2(ctx.mode, hop_instance, all_args, kwargs)

    from torch._higher_order_ops.effects import handle_effects

    return handle_effects(
        ctx.mode._allow_token_discovery,
        ctx.mode._tokens,
        invoke_leaf_function,
        all_args,
        kwargs,
    )

