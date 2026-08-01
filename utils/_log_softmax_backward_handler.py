
def _log_softmax_backward_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    grad_output = cast(DTensor, args[0])
    input_dtype = cast(torch.dtype, args[3])
    return grad_output.to(input_dtype)

