
def _is_valid_qconv_binary_optimization_pattern():
    return _is_valid_quantized_op_binary_optimization_pattern(
        torch.ops.onednn.qconv_pointwise
    )

