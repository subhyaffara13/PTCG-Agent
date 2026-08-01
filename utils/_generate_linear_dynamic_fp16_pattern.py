
def _generate_linear_dynamic_fp16_pattern(
    _dequant_weight_pattern,
    input_dim_exceeds_two=False,
    input_contiguous=True,
    relu_fused=False,
):
    dtype = torch.float32
    t_pattern = _generate_linear_t_pattern(_dequant_weight_pattern, dtype)

    if input_dim_exceeds_two and not input_contiguous:
        # pattern is
        #                   x -> expand -> bmm (-> add) (-> relu)
        # w -> dequant -> permute -> expand /
        pattern_no_bias = CallFunction(
            aten.bmm.default,
            CallFunction(
                aten.expand.default,
                KeywordArg("x"),
                KeywordArg("act_expand_size"),
            ),
            CallFunction(
                aten.expand.default,
                t_pattern,
                KeywordArg("wgt_expand_size"),
            ),
        )
        pattern_with_bias = CallFunction(
            aten.add.Tensor,
            pattern_no_bias,
            KeywordArg("b"),
        )
        if relu_fused:
            pattern_with_bias = CallFunction(aten.relu.default, pattern_with_bias)
            pattern_no_bias = CallFunction(aten.relu.default, pattern_no_bias)
        return pattern_with_bias, pattern_no_bias

    x_pattern_with_reshape = _may_generate_pattern_with_reshape(
        KeywordArg("x"),
        KeywordArg("act_reshape_size"),
        input_dim_exceeds_two,
    )
    dequant_linear_bias_pattern = generate_pattern_with_unary(
        _may_generate_pattern_with_reshape(
            CallFunction(
                aten.addmm.default,
                KeywordArg("b"),
                x_pattern_with_reshape,
                t_pattern,
            ),
            KeywordArg("output_reshape_size"),
            input_dim_exceeds_two,
        ),
        aten.relu.default if relu_fused else None,
    )
    dequant_linear_no_bias_pattern = generate_pattern_with_unary(
        _may_generate_pattern_with_reshape(
            CallFunction(
                aten.mm.default,
                x_pattern_with_reshape,
                t_pattern,
            ),
            KeywordArg("output_reshape_size"),
            input_dim_exceeds_two,
        ),
        aten.relu.default if relu_fused else None,
    )
    return dequant_linear_bias_pattern, dequant_linear_no_bias_pattern

