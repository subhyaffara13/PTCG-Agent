from typing import Any

def with_effects_functional(
    ctx,
    token: torch.Tensor,
    op: torch._ops.OpOverload,
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any],
) -> tuple[torch.Tensor, ...]:
    # with_effects is already functional, so just re-emit it.
    unwrapped_token, unwrapped_args, unwrapped_kwargs = ctx.unwrap_tensors(
        [token, args, kwargs]
    )
    with ctx.redispatch_to_next():
        result = with_effects(unwrapped_token, op, *unwrapped_args, **unwrapped_kwargs)
    return ctx.wrap_tensors(result)

