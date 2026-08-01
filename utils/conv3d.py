
def conv3d(
    input: list[int],
    weight: list[int],
    bias: Optional[list[int]],
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    groups: int,
):
    if len(weight) != 5:
        raise AssertionError(f"Expected 5D weight for conv3d, got {len(weight)}D")
    if len(input) != 5:
        raise AssertionError(f"Expected 5D input for conv3d, got {len(input)}D")
    return conv_output_size(input, weight, bias, stride, padding, dilation, groups)


def conv3d(
    g: jit_utils.GraphContext, input, weight, bias, stride, padding, dilation, groups
):
    str_padding = symbolic_helper._parse_arg(padding, "s")
    if str_padding in ["valid", "same"]:
        return _convolution_mode(
            g,
            input,
            weight,
            bias,
            stride,
            str_padding,
            dilation,
            groups,
        )
    else:
        padding = symbolic_helper._parse_arg(padding, "is")
        return _convolution(
            g,
            input,
            weight,
            bias,
            stride,
            padding,
            dilation,
            False,
            (),
            groups,
            None,
            None,
            None,
            None,
        )


def conv3d(
    input,
    weight,
    bias,
    stride=1,
    padding=0,
    dilation=1,
    groups=1,
    padding_mode="zeros",
    scale=1.0,
    zero_point=0,
    dtype=torch.quint8,
):
    r"""
    Applies a 3D convolution over a quantized 3D input composed of several input
    planes.

    See :class:`~torch.ao.nn.quantized.Conv3d` for details and output shape.

    Args:
        input: quantized input tensor of shape
          :math:`(\text{minibatch} , \text{in\_channels} , iD , iH , iW)`
        weight: quantized filters of shape
          :math:`(\text{out\_channels} , \frac{\text{in\_channels}}{\text{groups}} , kD , kH , kW)`
        bias: **non-quantized** bias tensor of shape
          :math:`(\text{out\_channels})`. The tensor type must be `torch.float`.
        stride: the stride of the convolving kernel. Can be a single number or a
          tuple `(sD, sH, sW)`. Default: 1
        padding: implicit paddings on both sides of the input. Can be a
          single number or a tuple `(padD, padH, padW)`. Default: 0
        dilation: the spacing between kernel elements. Can be a single number or
          a tuple `(dD, dH, dW)`. Default: 1
        groups: split input into groups, :math:`\text{in\_channels}` should be
          divisible by the number of groups. Default: 1
        padding_mode: the padding mode to use. Only "zeros" is supported for
          quantized convolution at the moment. Default: "zeros"
        scale: quantization scale for the output. Default: 1.0
        zero_point: quantization zero_point for the output. Default: 0
        dtype: quantization data type to use. Default: ``torch.quint8``

    Examples::

        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_QENGINE)
        >>> from torch.ao.nn.quantized import functional as qF
        >>> filters = torch.randn(8, 4, 3, 3, 3, dtype=torch.float)
        >>> inputs = torch.randn(1, 4, 5, 5, 5, dtype=torch.float)
        >>> bias = torch.randn(8, dtype=torch.float)
        >>>
        >>> scale, zero_point = 1.0, 0
        >>> dtype_inputs = torch.quint8
        >>> dtype_filters = torch.qint8
        >>>
        >>> q_filters = torch.quantize_per_tensor(filters, scale, zero_point, dtype_filters)
        >>> q_inputs = torch.quantize_per_tensor(inputs, scale, zero_point, dtype_inputs)
        >>> qF.conv3d(q_inputs, q_filters, bias, padding=1, scale=scale, zero_point=zero_point)
    """  # noqa: E501
    if padding_mode != "zeros":
        raise NotImplementedError("Only zero-padding is supported!")
    if input.dtype != torch.quint8:
        raise NotImplementedError(
            "Only torch.quint8 is supported for activation tensor!"
        )
    if weight.dtype != torch.qint8:
        raise NotImplementedError("Only torch.qint8 is supported for weight tensor!")
    if input.ndim != 5:
        raise ValueError("Input shape must be `(N, C, D, H, W)`!")
    stride = _triple(stride)
    padding = _triple(padding)
    dilation = _triple(dilation)

    packed_params = torch.ops.quantized.conv3d_prepack(
        weight, bias, stride, padding, dilation, groups
    )
    return torch.ops.quantized.conv3d(input, packed_params, scale, zero_point)

