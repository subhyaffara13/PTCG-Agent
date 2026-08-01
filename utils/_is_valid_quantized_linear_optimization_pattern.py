
def _is_valid_quantized_linear_optimization_pattern():
    def fn(match):
        output_dtype = _get_pattern_output_dtype(match)
        if output_dtype in [torch.float32, torch.bfloat16]:
            # Only keep matched pattern with same output_dtype
            qlinear_node_after_weight_prepack = filter_nodes(
                match.nodes, torch.ops.onednn.qlinear_pointwise
            )[0]
            return _check_node_kwarg_arg_value(
                qlinear_node_after_weight_prepack, "output_dtype", 9, output_dtype
            )
        return True

    return fn

