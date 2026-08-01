
def _generate_dequant_convolution_node_pattern(
    _dequant_per_channel_pattern, dtype=torch.float32, with_dtype_convert=False
):
    assert dtype in [torch.float32, torch.bfloat16]
    dequant_convolution_node_pattern = CallFunction(
        aten.convolution.default,
        _may_generate_pattern_with_dtype_convert(
            get_dequantize_per_tensor_activation_pattern(),
            KeywordArg("autocast_act_dtype"),
            with_dtype_convert,
        ),
        _dequant_per_channel_pattern,
        KeywordArg("b"),
        KeywordArg("stride"),
        KeywordArg("padding"),
        KeywordArg("dilation"),
        KeywordArg("is_transposed"),
        KeywordArg("out_padding"),
        KeywordArg("groups"),
    )
    return dequant_convolution_node_pattern

