
def _threshold(
    input: Tensor,
    threshold: float,
    value: float,
    inplace: bool = False,
) -> Tensor:
    r"""Apply a threshold to each element of the input Tensor.

    See :class:`~torch.nn.Threshold` for more details.
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            _threshold, (input,), input, threshold, value, inplace=inplace
        )
    if inplace:
        result = _VF.threshold_(input, threshold, value)
    else:
        result = _VF.threshold(input, threshold, value)
    return result

