
def _collapse_meta(a: Tensor, start: int, end: int) -> Tensor:
    # Special-case for zero dimensional tensors
    _validate_collapse_args(a, start, end)
    new_shape = _collapsed_shape(a.shape, start, end)
    return a.new_empty(new_shape)

