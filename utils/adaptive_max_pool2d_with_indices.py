
def adaptive_max_pool2d_with_indices(
    input: Tensor,
    output_size: BroadcastingList2[int],
    return_indices: bool = False,
) -> tuple[Tensor, Tensor]:  # noqa: D400
    r"""adaptive_max_pool2d(input, output_size, return_indices=False)

    Applies a 2D adaptive max pooling over an input signal composed of
    several input planes.

    See :class:`~torch.nn.AdaptiveMaxPool2d` for details and output shape.

    Args:
        output_size: the target output size (single integer or
            double-integer tuple)
        return_indices: whether to return pooling indices. Default: ``False``
    """
    if has_torch_function_unary(input):
        return handle_torch_function(
            adaptive_max_pool2d_with_indices,
            (input,),
            input,
            output_size,
            return_indices=return_indices,
        )
    # pyrefly: ignore [bad-argument-type]
    output_size = _list_with_default(output_size, input.size())
    return torch._C._nn.adaptive_max_pool2d(input, output_size)

