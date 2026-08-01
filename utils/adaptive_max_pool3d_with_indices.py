
def adaptive_max_pool3d_with_indices(
    input: Tensor,
    output_size: BroadcastingList3[int],
    return_indices: bool = False,
) -> tuple[Tensor, Tensor]:  # noqa: D400
    r"""
    adaptive_max_pool3d(input, output_size, return_indices=False)

    Applies a 3D adaptive max pooling over an input signal composed of
    several input planes.

    See :class:`~torch.nn.AdaptiveMaxPool3d` for details and output shape.

    Args:
        output_size: the target output size (single integer or
            triple-integer tuple)
        return_indices: whether to return pooling indices. Default: ``False``
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            adaptive_max_pool3d_with_indices,
            (input,),
            input,
            output_size,
            return_indices=return_indices,
        )
    # pyrefly: ignore [bad-argument-type]
    output_size = _list_with_default(output_size, input.size())
    return torch._C._nn.adaptive_max_pool3d(input, output_size)

