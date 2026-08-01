
def _transform_linear_with_packedparam(gm: torch.fx.GraphModule, node: torch.fx.Node):
    """Linear specific transformation function."""
    scale_node, zero_point_node = node.args[2], node.args[3]

    inp_node, param_node = node.args[0], node.args[1]
    if not isinstance(inp_node, torch.fx.Node):
        raise AssertionError(f"expected fx.Node for inp, got {type(inp_node)}")
    if not isinstance(param_node, torch.fx.Node):
        raise AssertionError(f"expected fx.Node for param, got {type(param_node)}")

    if param_node.op == "call_function":
        # Using LinearPrepackParam from linear_prepack.
        # We directly skip the packing call and inline weights and bias.
        w_node, b_node = param_node.args[0], param_node.args[1]
        if not isinstance(w_node, torch.fx.Node):
            raise AssertionError(f"expected fx.Node for w, got {type(w_node)}")
        if b_node is not None and not isinstance(b_node, torch.fx.Node):
            raise AssertionError(f"expected fx.Node for b, got {type(b_node)}")
        (
            param_0,
            param_1,
        ) = insert_weight_and_bias_get_attr_node_from_get_attr_to_qtensor(
            gm, w_node, b_node
        )
        op_res_node = gm.graph.call_function(
            torch.ops.aten.linear, (inp_node, param_0, param_1, *param_node.args[2:])
        )
    else:
        # Using LinearPackedParams.
        (
            param_0,
            param_1,
        ) = insert_weight_and_bias_get_attr_node_from_get_attr_to_scriptobject(
            gm, param_node
        )  # type: ignore[assignment]
        op_res_node = gm.graph.call_function(
            torch.ops.aten.linear, (inp_node, param_0, param_1)
        )
    return op_res_node, scale_node, zero_point_node

