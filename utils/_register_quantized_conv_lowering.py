
def _register_quantized_conv_lowering(
    pattern,
    pass_number,
    computation_op,
):
    @register_lowering_pattern(
        pattern,
        extra_check=_is_valid_qconv_lowering_pattern(),
        pass_number=pass_number,
    )
    def qconv(match: Match, *args, **kwargs):
        # Activation QParams
        x, x_scale, x_zp = (
            kwargs["x"],
            kwargs["x_scale"],
            kwargs["x_zp"],
        )
        # Weight QParams
        packed_weight, w_scale, w_zp = (
            kwargs["packed_weight"],
            kwargs["w_scale"],
            kwargs["w_zp"],
        )
        # Conv Params
        b, stride, padding, dilation, groups = (
            kwargs["b"],
            kwargs["stride"],
            kwargs["padding"],
            kwargs["dilation"],
            kwargs["groups"],
        )
        output_dtype = _get_pattern_output_dtype(match)
        assert output_dtype in [
            torch.int8,
            torch.uint8,
            torch.float8_e4m3fn,
            torch.float32,
            torch.bfloat16,
        ]
        # Output QParams
        o_inv_scale = kwargs["output_scale"]
        o_zero_point = kwargs["output_zero_point"]
        output_dtype = kwargs["output_dtype"]
        # post op
        postop_name = kwargs["postop_name"]
        postop_args = kwargs["postop_args"]
        postop_algorithm = kwargs["postop_algorithm"]

        computation_args = (
            x,
            x_scale,
            x_zp,
            packed_weight,
            w_scale,
            w_zp,
            b,
            stride,
            padding,
            dilation,
            groups,
            o_inv_scale,
            o_zero_point,
            output_dtype,
            postop_name,
            postop_args,
            postop_algorithm,
        )
        counters["inductor"]["qconv_unary_lower_count"] += 1
        counters["inductor"]["qconv_unary_lower_nodes"] += len(match.nodes)
        return L[computation_op](*computation_args)

    return qconv

