
def _consecutive_return_inverse(
    input,
    return_inverse=False,
    return_counts=False,
    dim=None,
):
    # type: (Tensor, bool, bool, Optional[int]) -> tuple[Tensor, Tensor]

    if has_torch_function_unary(input):
        return _unique_consecutive_impl(input, return_inverse, return_counts, dim)

    output, inverse_indices, _ = _unique_consecutive_impl(
        input, return_inverse, return_counts, dim
    )
    return output, inverse_indices

