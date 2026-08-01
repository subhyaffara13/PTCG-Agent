
def _generate_dequant_bmm_node_pattern(
    _dequant_per_channel_pattern,
    dtype=torch.float32,
    with_bias=False,
    is_tensor_overload=False,
    with_dtype_convert=False,
):
    # When activation of linear dim exceed 2 and not contiguous
    t_pattern = _generate_linear_t_pattern(_dequant_per_channel_pattern, dtype)

    assert dtype in [torch.float32, torch.bfloat16]
    dequant_bmm_pattern = CallFunction(
        aten.bmm.default,
        CallFunction(
            aten.expand.default,
            _may_generate_pattern_with_dtype_convert(
                get_dequantize_per_tensor_activation_pattern(is_tensor_overload),
                KeywordArg("autocast_act_dtype"),
                with_dtype_convert,
            ),
            KeywordArg("act_expand_size"),
        ),
        CallFunction(
            aten.expand.default,
            t_pattern,
            KeywordArg("wgt_expand_size"),
        ),
    )

    def _generate_pattern_with_output_add(_dequant_bmm_pattern, _with_bias):
        if _with_bias:
            return CallFunction(
                aten.add.Tensor,
                _dequant_bmm_pattern,
                KeywordArg("b"),
            )
        else:
            return _dequant_bmm_pattern

    return _generate_pattern_with_output_add(dequant_bmm_pattern, with_bias)

