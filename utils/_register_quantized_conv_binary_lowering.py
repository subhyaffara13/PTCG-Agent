
def _register_quantized_conv_binary_lowering(
    pattern,
    pass_number,
    computation_op,
):
    @register_lowering_pattern(
        pattern,
        extra_check=_is_valid_qconv_lowering_pattern(),
        pass_number=pass_number,
    )
    def qconv_binary(match: Match, *args, **kwargs):
        output_dtype = _get_pattern_output_dtype(match)
        assert output_dtype is not None
        x, x_scale, x_zp = kwargs["x"], kwargs["x_scale"], kwargs["x_zp"]
        accum = kwargs["accum"]
        accum_scale = kwargs["accum_scale"]
        accum_zp = kwargs["accum_zero_point"]
        packed_weight, w_scale, w_zp = (
            kwargs["packed_weight"],
            kwargs["w_scale"],
            kwargs["w_zp"],
        )
        b, stride, padding, dilation, groups = (
            kwargs["b"],
            kwargs["stride"],
            kwargs["padding"],
            kwargs["dilation"],
            kwargs["groups"],
        )
        # Output QParams
        output_scale = kwargs["output_scale"]
        output_zero_point = kwargs["output_zero_point"]

        # post ops
        binary_op_name = kwargs["binary_op_name"]
        alpha = kwargs["alpha"]
        unary_op_name = kwargs["unary_op_name"]
        unary_op_args = kwargs["unary_op_args"]
        unary_op_algorithm = kwargs["unary_op_algorithm"]

        accum.realize()
        from .mkldnn_fusion import _can_be_inplace

        assert _can_be_inplace(accum), (
            "QConv Binary Inplace Fusion requires accum is not an alias or mutation."
        )

        computation_args = (
            x,
            x_scale,
            x_zp,
            packed_weight,
            w_scale,
            w_zp,
            accum,
            b,
            stride,
            padding,
            dilation,
            groups,
            output_scale,
            output_zero_point,
            output_dtype,
            accum_scale,
            accum_zp,
            binary_op_name,
            alpha,
            unary_op_name,
            unary_op_args,
            unary_op_algorithm,
        )
        counters["inductor"]["qconv2d_binary_lower_count"] += 1
        counters["inductor"]["qconv2d_binary_lower_nodes"] += len(match.nodes)
        return L[computation_op](*computation_args)

    return qconv_binary

