
def should_pad(
    match: Match,
    mat1: Tensor,
    mat2: Tensor,
    op: torch._ops.OpOverloadPacket,
    input: Tensor | None = None,
) -> bool:
    _can_pad = can_pad(mat1, mat2, op, input)
    # Note that if you're tempted to insert a dynamo_timed call here, this function can
    # be called enough that the dynamo_timed overhead is not negligible.
    return _can_pad and _should_pad(match, mat1, mat2, op, input)

