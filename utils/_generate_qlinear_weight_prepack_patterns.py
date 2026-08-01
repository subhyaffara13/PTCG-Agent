
def _generate_qlinear_weight_prepack_patterns(
    dtype=torch.float32,
    input_dim_exceeds_two=False,
    input_contiguous=True,
    with_bias=False,
    is_tensor_overload=False,
    with_dtype_convert=False,
):
    if input_dim_exceeds_two and not input_contiguous:
        return _generate_dequant_bmm_node_pattern(
            dequantize_per_channel_weight_pattern,
            dtype,
            with_bias,
            is_tensor_overload,
            with_dtype_convert,
        )
    else:
        return _generate_dequant_linear_node_pattern(
            dequantize_per_channel_weight_pattern,
            dtype,
            input_dim_exceeds_two,
            is_tensor_overload,
            with_dtype_convert,
        )

