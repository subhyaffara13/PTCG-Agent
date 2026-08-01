
def _return_inverse(
    input,
    sorted=True,
    return_inverse=False,
    return_counts=False,
    dim=None,
):
    # type: (Tensor, bool, bool, bool, Optional[int]) -> tuple[Tensor, Tensor]

    if has_torch_function_unary(input):
        return _unique_impl(input, sorted, return_inverse, return_counts, dim)

    output, inverse_indices, _ = _unique_impl(
        input, sorted, return_inverse, return_counts, dim
    )
    return output, inverse_indices

