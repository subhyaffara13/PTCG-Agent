
def _register_dequant_promotion():
    dequant_pattern_cases = itertools.product(
        [torch.float32, torch.bfloat16], [True, False], [True, False]
    )
    for dtype, input_dim_exceeds_two, is_tensor_overload in dequant_pattern_cases:
        # 4 dequantization patterns will be matched based on the dtype and input dimension size.
        # Case 1: int8-mixed-fp32, input dim size is 2
        # Case 2: int8-mixed-fp32, input dim size exceeds 2
        # Case 3: int8-mixed-bf16, input dim size is 2
        # Case 4: int8-mixed-bf16, input dim size exceeds 2
        #           quant
        #   + - - - - | - - - - +
        #   |      dequant      |
        #   |         |         |
        #   |    OPT(to_bf16)   |
        #   |         |         |
        #   |    OPT(reshape)   |
        #   |      /     \      |
        #   |    node1  node2   |
        #   + - - | - - - | - - +
        #  OPT(reshape) OPT(reshape)
        #   + - - | - - - | - - +
        #  OPT(to_fp32) OPT(to_fp32)
        #   + - - | - - - | - - +
        #       quant   quant
        _register_dequant_promotion_pass(
            _may_generate_pattern_with_reshape(
                _may_generate_pattern_with_dtype_convert(
                    get_dequantize_per_tensor_activation_pattern(
                        is_tensor_overload=is_tensor_overload
                    ),
                    KeywordArg("autocast_act_dtype"),
                    dtype == torch.bfloat16,
                ),
                KeywordArg("act_reshape_size"),
                with_reshape=input_dim_exceeds_two,
            ),
            pass_number=0,
            dtype=dtype,
        )  # pass_number=0 to run before weight prepack

