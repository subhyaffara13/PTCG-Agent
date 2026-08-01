
def call_torchbind_func(ctx, *args, **kwargs):
    from torch._higher_order_ops.effects import handle_effects

    return handle_effects(
        ctx.mode._allow_token_discovery, ctx.mode._tokens, call_torchbind, args, kwargs
    )

