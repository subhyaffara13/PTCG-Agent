
def _consecutive_return_counts(
    input,
    return_inverse=False,
    return_counts=False,
    dim=None,
):
    # type: (Tensor, bool, bool, Optional[int]) -> tuple[Tensor, Tensor]

    if has_torch_function_unary(input):
        return _unique_consecutive_impl(input, return_inverse, return_counts, dim)

    output, _, counts = _unique_consecutive_impl(
        input, return_inverse, return_counts, dim
    )
    return output, counts

