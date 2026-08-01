
def adaptive_avg_pool3d(input: Tensor, output_size: BroadcastingList3[int]) -> Tensor:
    r"""Apply a 3D adaptive average pooling over an input signal composed of several input planes.

    See :class:`~torch.nn.AdaptiveAvgPool3d` for details and output shape.

    Args:
        output_size: the target output size (single integer or
            triple-integer tuple)
    """
    if has_torch_function_unary(input):
        return handle_torch_function(adaptive_avg_pool3d, (input,), input, output_size)
    # pyrefly: ignore [bad-argument-type]
    _output_size = _list_with_default(output_size, input.size())
    return torch._C._nn.adaptive_avg_pool3d(input, _output_size)


def adaptive_avg_pool3d(input: Tensor, output_size: BroadcastingList2[int]) -> Tensor:
    r"""
    Applies a 3D adaptive average pooling over a quantized input signal composed
    of several quantized input planes.

    .. note:: The input quantization parameters propagate to the output.

    See :class:`~torch.ao.nn.quantized.AdaptiveAvgPool3d` for details and output shape.

    Args:
        output_size: the target output size (single integer or
                     double-integer tuple)
    """
    if not input.is_quantized:
        raise ValueError(
            "Input to 'quantized.functional.adaptive_avg_pool3d' must be quantized!"
        )
    return torch.nn.functional.adaptive_avg_pool3d(input, output_size)

