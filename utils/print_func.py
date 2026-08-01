
def print_func(ctx, format_str: str, *args: object, **kwargs: object):
    from torch._higher_order_ops.effects import handle_effects

    return handle_effects(
        ctx.mode._allow_token_discovery,
        ctx.mode._tokens,
        print,  # type: ignore[arg-type]
        (format_str, *args),
        kwargs,  # type: ignore[arg-type]
    )

