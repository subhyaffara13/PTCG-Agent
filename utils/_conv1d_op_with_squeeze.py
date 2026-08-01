
def _conv1d_op_with_squeeze(
    inp: torch.Tensor,
    weight: torch.Tensor,
    bias: torch.Tensor | None,
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    groups: int,
) -> torch.Tensor:
    # In quantized version, conv1d is emulated using conv2d with squeeze and unsqueeze
    # operations before and after the conv2d operation to match the dimension of weights.
    # Reference: https://github.com/pytorch/pytorch/blob/eca0cb0fbe84bb0a34fa94afe261bceecd52c436/aten/src/ATen/native/quantized/cpu/qconv.cpp#L1827  # noqa: B950
    s_inp = torch.ops.aten.unsqueeze(inp, 2)
    conv1d_res = torch.ops.aten.conv2d(
        s_inp,
        weight,
        bias,
        stride,
        padding,
        dilation,
        groups,
    )
    uns_conv1d_res = torch.ops.aten.squeeze(conv1d_res, 2)
    return uns_conv1d_res

