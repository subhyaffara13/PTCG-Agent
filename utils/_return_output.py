
def _return_output(
    input,
    sorted=True,
    return_inverse=False,
    return_counts=False,
    dim=None,
):
    # type: (Tensor, bool, bool, bool, Optional[int]) -> Tensor

    if has_torch_function_unary(input):
        return _unique_impl(input, sorted, return_inverse, return_counts, dim)

    output, _, _ = _unique_impl(input, sorted, return_inverse, return_counts, dim)
    return output

