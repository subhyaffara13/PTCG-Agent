
def adaptive_max_pool1d_with_indices(
    input: Tensor,
    output_size: BroadcastingList1[int],
    return_indices: bool = False,
) -> tuple[Tensor, Tensor]:  # noqa: D400
    r"""
    adaptive_max_pool1d(input, output_size, return_indices=False)

    Applies a 1D adaptive max pooling over an input signal composed of
    several input planes.

    See :class:`~torch.nn.AdaptiveMaxPool1d` for details and output shape.

    Args:
        output_size: the target output size (single integer)
        return_indices: whether to return pooling indices. Default: ``False``
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            adaptive_max_pool1d_with_indices,
            (input,),
            input,
            output_size,
            return_indices=return_indices,
        )
    return torch.adaptive_max_pool1d(input, output_size)

