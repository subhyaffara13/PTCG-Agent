
def _register_quantized_linear_binary_lowering(
    pattern,
    pass_number,
    computation_op,
):
    @register_lowering_pattern(
        pattern,
        extra_check=_is_valid_qlinear_lowering_pattern(),
        pass_number=pass_number,
    )
    def qlinear_binary(match: Match, *args, **kwargs):
        output_dtype = _get_pattern_output_dtype(match)
        assert output_dtype is not None
        # Activation QParams
        x, x_scale, x_zp = (
            kwargs["x"],
            kwargs["x_scale"],
            kwargs["x_zp"],
        )
        x2 = kwargs["x_2"]
        x2_scale = kwargs["x2_scale"]
        x2_zp = kwargs["x2_zp"]
        # Weight QParams
        packed_weight, w_scale, w_zp = (
            kwargs["packed_weight"],
            kwargs["w_scale"],
            kwargs["w_zp"],
        )
        # bias
        b = kwargs.get("b")
        # Output QParams
        o_inv_scale = kwargs["output_scale"]
        o_zero_point = kwargs["output_zero_point"]

        x2.realize()
        from .mkldnn_fusion import _qlinear_binary_can_be_inplace

        binary_op_name = kwargs["binary_op_name"]
        alpha = kwargs["alpha"]
        unary_op_name = kwargs["unary_op_name"]
        unary_op_args = kwargs["unary_op_args"]
        unary_op_algorithm = kwargs["unary_op_algorithm"]
        if (
            # TODO Ensure sum is safe and remove such check, i.e.,
            # x2 is not used by other operations
            # or current qlinear sum is the last user of x2.
            # This needs to be ensured when registering
            # the lowering pattern of quantized_linear_binary.
            binary_op_name == "sum" and (not _qlinear_binary_can_be_inplace(x2))
        ):
            binary_op_name = "add"

        computation_args = (
            x,
            x_scale,
            x_zp,
            packed_weight,
            w_scale,
            w_zp,
            x2,
            b,
            o_inv_scale,
            o_zero_point,
            output_dtype,
            x2_scale,
            x2_zp,
            binary_op_name,
            alpha,
            unary_op_name,
            unary_op_args,
            unary_op_algorithm,
        )
        counters["inductor"]["qlinear_binary_lower_count"] += 1
        counters["inductor"]["qlinear_binary_lower_nodes"] += len(match.nodes)
        return L[computation_op](*computation_args)

    return qlinear_binary

