
def meta_conv(
    input_tensor: torch.Tensor,
    weight: torch.Tensor,
    bias: torch.Tensor,
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    is_transposed: bool,
    output_padding: list[int],
    groups: int,
):
    shape_out = calc_conv_nd_return_shape(
        input_tensor,
        weight,
        stride,
        padding,
        dilation,
        is_transposed,
        groups,
        output_padding if is_transposed else None,
    )

    from torch.fx.experimental.symbolic_shapes import guard_or_false

    input_channels_dim = 1
    output_channels_dim = 1
    if guard_or_false(input_tensor.size(input_channels_dim) == 0):
        shape_out[output_channels_dim] = 0

    # Memory format is left as contiguous: meta tensors have no device info,
    # so _select_conv_backend returns Overrideable and the correct format
    # cannot be determined here.  The FakeTensor path (torch.compile, export)
    # intercepts via a register_op_impl in fake_impls.py before reaching this
    # kernel and uses FakeTensor.fake_device for an accurate answer.
    out = input_tensor.new_empty(shape_out)
    return out

