
def _is_valid_qconv_post_op_fusion_pattern(has_binary_post_op=False):
    return (
        _is_valid_qconv_binary_optimization_pattern()
        if has_binary_post_op
        else _is_valid_quantized_conv_optimization_pattern()
    )

