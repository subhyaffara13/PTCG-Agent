
def _floor_divide_integer(a: Tensor, b: Tensor) -> Tensor:
    a, b = _maybe_broadcast(a, b)

    if not a.dtype.is_signed:
        return prims.div(a, b)

    # Convert truncation to flooring:
    offset = (torch.signbit(a) != torch.signbit(b)).logical_and(torch.fmod(a, b) != 0)
    return prims.div(a, b) - _maybe_convert_to_dtype(offset, a.dtype)

