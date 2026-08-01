
def is_pinned_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> bool:
    tensor = cast(dtensor.DTensor, args[0])
    return tensor._local_tensor.is_pinned()

