
def _generate_dequant_linear_node_pattern(
    _dequant_per_channel_pattern,
    dtype=torch.float32,
    input_dim_exceeds_two=False,
    is_tensor_overload=False,
    with_dtype_convert=False,
):
    assert dtype in [torch.float32, torch.bfloat16]
    t_pattern = _generate_linear_t_pattern(_dequant_per_channel_pattern, dtype)
    dequant_linear_bias_pattern = _may_generate_pattern_with_reshape(
        CallFunction(
            aten.addmm.default,
            KeywordArg("b"),
            _may_generate_pattern_with_reshape(
                _may_generate_pattern_with_dtype_convert(
                    get_dequantize_per_tensor_activation_pattern(is_tensor_overload),
                    KeywordArg("autocast_act_dtype"),
                    with_dtype_convert,
                ),
                KeywordArg("act_reshape_size"),
                input_dim_exceeds_two,
            ),
            t_pattern,
        ),
        KeywordArg("output_reshape_size"),
        input_dim_exceeds_two,
    )
    dequant_linear_no_bias_pattern = _may_generate_pattern_with_reshape(
        CallFunction(
            aten.mm.default,
            _may_generate_pattern_with_reshape(
                _may_generate_pattern_with_dtype_convert(
                    get_dequantize_per_tensor_activation_pattern(is_tensor_overload),
                    KeywordArg("autocast_act_dtype"),
                    with_dtype_convert,
                ),
                KeywordArg("act_reshape_size"),
                input_dim_exceeds_two,
            ),
            t_pattern,
        ),
        KeywordArg("output_reshape_size"),
        input_dim_exceeds_two,
    )
    return dequant_linear_bias_pattern, dequant_linear_no_bias_pattern

