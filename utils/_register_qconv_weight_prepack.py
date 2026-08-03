import itertools

def _register_qconv_weight_prepack():
    for dtype, with_dtype_convert in itertools.product(
        [torch.float32, torch.bfloat16], [True, False]
    ):
        if dtype == torch.float32 and with_dtype_convert:
            continue
        weight_prepack_patterns = _generate_qconv_weight_prepack_patterns(
            dtype, with_dtype_convert
        )
        for weight_prepack_pattern in weight_prepack_patterns:
            # Register to pass_number 1, so we can do dequant promotion in pass_number 0.
            _register_qconv_weight_prepack_pass(
                weight_prepack_pattern,
                pass_number=1,
                dtype=dtype,
                with_dtype_convert=with_dtype_convert,
            )

