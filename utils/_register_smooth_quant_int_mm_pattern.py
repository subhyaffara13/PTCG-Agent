
def _register_smooth_quant_int_mm_pattern():
    """
    The pattern is:
      (no bias) reshape -> _int_mm -> convert_element_type -> (expand ->) mul -> mul -> reshape
    or
      (with bias) pattern_no_bias -> add (-> reshape -> reshape)
    """

    # When torch.compile'ing with dynamic=True, the expand node and the two tailing reshape nodes exist
    # When torch.compile'ing with dynamic=False, they don't exist
    def get_pattern_no_bias(expand_a_scale: bool, reshape_a: bool = True):
        return CallFunction(
            aten.mul.Tensor,
            CallFunction(
                aten.mul.Tensor,
                CallFunction(
                    prims.convert_element_type.default,
                    CallFunction(
                        aten._int_mm.default,
                        CallFunction(
                            aten.reshape.default,
                            KeywordArg("a"),
                            KeywordArg("in_shape"),
                        )
                        if reshape_a
                        else KeywordArg("a"),
                        KeywordArg("b"),
                    ),
                    KeywordArg("dtype"),
                ),
                (
                    CallFunction(
                        aten.expand.default,
                        KeywordArg("x_scale"),
                        Arg(),
                    )
                    if expand_a_scale
                    else KeywordArg("x_scale")
                ),
            ),
            KeywordArg("w_scale"),
        )

    def _with_outer_reshape(pattern):
        return CallFunction(
            aten.reshape.default, pattern, KeywordArg("out_shape_no_bias")
        )

    # for torch.compile(dynamic=False)
    pattern_no_bias_1 = _with_outer_reshape(get_pattern_no_bias(expand_a_scale=False))
    pattern_with_bias_1 = CallFunction(
        aten.add.Tensor,
        pattern_no_bias_1,
        KeywordArg("bias"),
    )
    # for torch.compile(dynamic=True)
    pattern_no_bias_2 = _with_outer_reshape(get_pattern_no_bias(expand_a_scale=True))
    pattern_with_bias_2 = CallFunction(
        aten.reshape.default,
        CallFunction(
            aten.reshape.default,
            CallFunction(
                aten.add.Tensor,
                pattern_no_bias_2,
                KeywordArg("bias"),
            ),
            Arg(),
        ),
        KeywordArg("out_shape_with_bias"),
    )

    # The following patterns are for torchao int8_dynamic_activation_int8_weight linear,
    # when both activation and weights are symmetrically quantized.
    # In practice, though, they may also match smooth-quant pattern when a 2D input shape would be used.
    # Since add is not currently being used as a oneDNN post-op, but is unfused, we don't need these patterns with bias.
    # Ideally, we should add mul + add post-op support in ATen int8 oneDNN linear op.
    pattern1_with_no_outer_or_act_reshape = get_pattern_no_bias(
        expand_a_scale=False, reshape_a=False
    )
    pattern2_with_no_outer_or_act_reshape = get_pattern_no_bias(
        expand_a_scale=True, reshape_a=False
    )

    def _validate_pattern(match: Match):
        if len(match.nodes) not in [4, 5, 6, 7, 10]:
            return False
        # Make sure weight is a constant
        aten_int_mm_node = filter_nodes(match.nodes, aten._int_mm.default)[0]
        if not isinstance(aten_int_mm_node.args[1], torch.fx.node.Node):
            return False
        if aten_int_mm_node.args[1].op != "get_attr":
            return False

        if len(match.nodes) == 10:
            # Check the two tailing reshape nodes can be fused
            if match.nodes[9].args[1] != match.nodes[6].args[1]:
                return False
        if len(match.nodes) == 10 or (
            len(match.nodes) == 7 and match.nodes[6].target is aten.add.Tensor
        ):
            bias_idx = 7 if len(match.nodes) == 10 else 6
            # Check bias shape
            bias_node = match.nodes[bias_idx].args[1]
            if not isinstance(bias_node, torch.fx.node.Node):
                return False
            if len(bias_node.meta.get("tensor_meta").shape) != 1:  # type: ignore[union-attr]
                return False
        return True

    pattern_to_pass_number = {
        pattern_no_bias_2: 0,
        pattern_with_bias_2: 0,
        pattern_no_bias_1: 1,
        pattern_with_bias_1: 1,
        pattern1_with_no_outer_or_act_reshape: 2,
        pattern2_with_no_outer_or_act_reshape: 2,
    }
    for pattern, pass_number in pattern_to_pass_number.items():

        @register_freezing_graph_pattern(
            pattern,
            extra_check=_validate_pattern,
            pass_number=pass_number,
        )
        def _int_mm_weight_prepack(match: Match, *args, **kwargs):
            bias = kwargs.get("bias")
            x = kwargs["a"]
            weight = kwargs["b"]
            dtype = kwargs["dtype"]
            x_scale = kwargs["x_scale"]
            w_scale = kwargs["w_scale"]
            x_shape = x.meta.get("tensor_meta").shape
            if has_free_symbols(x_shape):
                # For dynamic shape case, we can't get activation shape ahead of runtime.
                x_shape = None

            out_node = match.output_node()
            with match.graph.inserting_before(out_node):
                transpose_node = match.graph.call_function(
                    aten.permute.default, args=(weight, [1, 0])
                )
                contig_node = match.graph.call_function(
                    aten.contiguous.default, args=(transpose_node,)
                )
                packed_weight_inputs = (
                    contig_node,
                    x_shape,
                )
                packed_weight_op = torch.ops.onednn.qlinear_prepack
                prepack_weight_node = match.graph.call_function(
                    packed_weight_op, args=packed_weight_inputs
                )

                dummy_zp = None
                w_scale = match.graph.call_function(
                    prims.convert_element_type.default, args=(w_scale, torch.float32)
                )

                x_scale_shape = x_scale.meta.get("tensor_meta").shape
                x_scale_is_scalar = False
                if not has_free_symbols(x_scale_shape):
                    prod = 1
                    for d in x_scale_shape:
                        prod *= d
                    x_scale_is_scalar = prod == 1

                new_args: tuple[Any, ...]
                if x_scale_is_scalar:
                    # in this case, we can call onednn.qlinear directly
                    new_args = (
                        x,
                        x_scale,
                        dummy_zp,  # x_zp
                        prepack_weight_node,
                        w_scale,
                        dummy_zp,  # w_zp
                        bias,
                        1.0,  # output_scale
                        0,  # output_zero_point
                        dtype,  # output_dtype
                        "none",  # post op name
                        [],  # post op args
                        "",  # post op algorithm
                    )
                    new_linear_node = match.graph.call_function(
                        torch.ops.onednn.qlinear_pointwise.tensor, args=new_args
                    )
                    out_node.replace_all_uses_with(new_linear_node)
                    new_linear_node.meta.update(out_node.meta)
                else:
                    # onednn.qlinear does not support per-channel quantization of x
                    # so in this case, we have to apply x scale and add bias ourselves after qlinear
                    in_shape = kwargs.get("in_shape")
                    if in_shape is None:
                        x_reshaped = x
                    else:
                        x_reshaped = match.graph.call_function(
                            aten.reshape.default, args=(x, in_shape)
                        )
                    new_args = (
                        x_reshaped,
                        1.0,  # x_scale
                        0,  # x_zp
                        prepack_weight_node,
                        w_scale,
                        dummy_zp,  # w_zp
                        None,  # bias
                        1.0,  # output_scale
                        0,  # output_zero_point
                        dtype,  # output_dtype
                        "none",  # post op name
                        [],  # post op args
                        "",  # post op algorithm
                    )
                    new_linear_node = match.graph.call_function(
                        torch.ops.onednn.qlinear_pointwise, args=new_args
                    )
                    # apply x scale
                    new_out_node = match.graph.call_function(
                        aten.mul.Tensor, args=(new_linear_node, x_scale)
                    )

                    # Add bias and reshape
                    has_outer_reshape = (
                        kwargs.get("out_shape_with_bias") is not None
                        or kwargs.get("out_shape_no_bias") is not None
                    )

                    if has_outer_reshape:
                        out_shape = kwargs.get(
                            "out_shape_with_bias", kwargs["out_shape_no_bias"]
                        )
                    if bias is not None:
                        new_out_node = match.graph.call_function(
                            aten.add.Tensor, args=(new_out_node, bias)
                        )
                        if has_outer_reshape:
                            new_out_node = match.graph.call_function(
                                aten.reshape.default,
                                args=(new_out_node, out_shape),  # type: ignore[possibly-undefined]
                            )
                    else:
                        if has_outer_reshape:
                            new_out_node = match.graph.call_function(
                                aten.reshape.default,
                                args=(new_out_node, out_shape),  # type: ignore[possibly-undefined]
                            )
                    out_node.replace_all_uses_with(new_out_node)
                    new_out_node.meta.update(out_node.meta)
                for node in reversed(match.nodes):
                    match.graph.erase_node(node)
                counters["inductor"]["qlinear_weight_prepack_matcher_count"] += 1
                counters["inductor"]["qlinear_weight_prepack_matcher_nodes"] += len(
                    match.nodes
                )

