import itertools

def _register_linear_dynamic_fp16_weight_prepack():
    to_dtype_op = torch.ops.quantized_decomposed.convert_element_type.no_fuse
    weight_pattern = CallFunction(
        to_dtype_op,
        CallFunction(
            to_dtype_op,
            KeywordArg("w"),
            KeywordArg("dtype_fp16"),
        ),
        KeywordArg("dtype_fp32"),
    )
    cases = itertools.product(
        [False, True],  # input_dim_exceeds_two
        [True, False],  # input_contiguous
        [False, True],  # relu fused
    )
    for input_dim_exceeds_two, input_contiguous, relu_fused in cases:
        patterns = _generate_linear_dynamic_fp16_pattern(
            weight_pattern,
            input_dim_exceeds_two,
            input_contiguous,
            relu_fused,
        )
        for pattern in patterns:
            _register_linear_dynamic_fp16_weight_prepack_pass(
                pattern,
                pass_number=0 if relu_fused else 1,
                input_dim_exceeds_two=input_dim_exceeds_two,
                input_contiguous=input_contiguous,
                relu_fused=relu_fused,
            )

