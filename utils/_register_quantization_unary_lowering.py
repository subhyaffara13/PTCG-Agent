import itertools

def _register_quantization_unary_lowering():
    # QConv2d
    for x_scale_zp_are_tensors, users in itertools.product([False, True], [1, 2]):
        qconv_pattern = get_qconv_pt2e_pattern(x_scale_zp_are_tensors, users)
        computation_op = (
            torch.ops.onednn.qconv_pointwise.tensor
            if x_scale_zp_are_tensors
            else torch.ops.onednn.qconv_pointwise.default
        )
        _register_quantized_conv_lowering(
            qconv_pattern,
            2,  # pass_number
            computation_op,
        )

    # QLinear
    for x_scale_zp_are_tensors in (False, True):
        qlinear_pattern = get_qlinear_pt2e_pattern(x_scale_zp_are_tensors)
        computation_op = (
            torch.ops.onednn.qlinear_pointwise.tensor
            if x_scale_zp_are_tensors
            else torch.ops.onednn.qlinear_pointwise.default
        )
        _register_quantized_linear_unary_lowering(
            qlinear_pattern,
            2,  # pass_number
            computation_op,
        )

