
def with_effects_dense(
    token: torch.Tensor,
    op: torch._ops.OpOverload,
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any],
) -> tuple[torch.Tensor, ...]:
    out = op(*args, **kwargs)
    new_token = new_token_tensor()
    # [NOTE: with_effects return type]
    # Note that we should only do *out for tuple type, but not list type.
    # This is to match the schema of the op.
    # For tuple output, the length of schema output is the same as the length of out.
    # For list output, the length of schema output is 1 (e.g. Tensor[]) regardless of the
    # length of the list.
    if isinstance(out, tuple):
        return (new_token, *out)
    return (new_token, out)

