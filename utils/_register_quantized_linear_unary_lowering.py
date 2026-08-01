
def _register_quantized_linear_unary_lowering(
    pattern,
    pass_number,
    computation_op,
):
    @register_lowering_pattern(
        pattern,
        extra_check=_is_valid_qlinear_lowering_pattern(),
        pass_number=pass_number,
    )
    def qlinear(match: Match, *args, **kwargs):
        output_dtype = _get_pattern_output_dtype(match)
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

        # bias
        b = kwargs.get("b")

        # Output QParams
        o_inv_scale = kwargs["output_scale"]
        o_zero_point = kwargs["output_zero_point"]

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
            o_inv_scale,
            o_zero_point,
            output_dtype,
            postop_name,
            postop_args,
            postop_algorithm,
        )
        counters["inductor"]["qlinear_unary_lower_count"] += 1
        counters["inductor"]["qlinear_unary_lower_nodes"] += len(match.nodes)
        return L[computation_op](*computation_args)

    return qlinear

