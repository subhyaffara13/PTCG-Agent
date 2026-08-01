
def _consecutive_return_output(
    input,
    return_inverse=False,
    return_counts=False,
    dim=None,
):
    # type: (Tensor, bool, bool, Optional[int]) -> Tensor

    if has_torch_function_unary(input):
        return _unique_consecutive_impl(input, return_inverse, return_counts, dim)

    output, _, _ = _unique_consecutive_impl(input, return_inverse, return_counts, dim)
    return output

