
def _generate_linear_t_pattern(
    _dequant_per_channel_pattern,
    dtype,
):
    assert dtype in [torch.float32, torch.bfloat16]
    t_pattern = CallFunction(
        aten.permute.default,
        _may_generate_pattern_with_dtype_convert(
            _dequant_per_channel_pattern,
            KeywordArg("autocast_wgt_dtype"),
            dtype == torch.bfloat16,
        ),
        KeywordArg("permute_axes"),
    )
    return t_pattern

