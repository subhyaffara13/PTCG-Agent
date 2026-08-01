
def _is_valid_qlinear_post_op_fusion_pattern(has_binary_post_op=False):
    return (
        _is_valid_qlinear_binary_optimization_pattern()
        if has_binary_post_op
        else _is_valid_quantized_linear_optimization_pattern()
    )

