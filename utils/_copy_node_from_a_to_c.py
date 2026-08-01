
def _copy_node_from_a_to_c(
    node_a: Node,
    gm_a: GraphModule,
    gm_b: GraphModule,
    graph_c: Graph,
) -> Node:
    """
    Simple copy of node_a to graph_c.
    """
    if node_a.op == "get_attr":
        node_a_copy_name = get_new_attr_name_with_prefix(node_a.name + "_shadow_copy_")(
            gm_b
        )
        node_a_obj = getattr_from_fqn(gm_a, node_a.target)  # type: ignore[arg-type]
        if torch.is_tensor(node_a_obj):
            node_a_obj = node_a_obj.detach()
        setattr(gm_b, node_a_copy_name, node_a_obj)
        node_a_copy = graph_c.create_node(
            node_a.op, node_a_copy_name, (), {}, node_a_copy_name
        )
        return node_a_copy
    elif node_a.op == "call_method":
        if node_a.target not in ("dequantize", "to"):
            raise AssertionError(f"target {node_a.target} is not implemented")
        if node_a.target == "dequantize":
            arg_copy = _copy_node_from_a_to_c(
                get_normalized_nth_input(node_a, gm_a, 0), gm_a, gm_b, graph_c
            )  # type: ignore[arg-type]
            node_a_copy_name = get_new_attr_name_with_prefix(
                node_a.name + "_shadow_copy_"
            )(gm_b)
            node_a_copy = graph_c.create_node(
                node_a.op, node_a.target, (arg_copy,), {}, node_a_copy_name
            )
            return node_a_copy
        else:  # to
            arg_copy = _copy_node_from_a_to_c(
                get_normalized_nth_input(node_a, gm_a, 0), gm_a, gm_b, graph_c
            )  # type: ignore[arg-type]
            node_a_copy_name = get_new_attr_name_with_prefix(
                node_a.name + "_shadow_copy_"
            )(gm_b)
            node_a_copy = graph_c.create_node(
                node_a.op,
                node_a.target,
                (arg_copy, get_normalized_nth_input(node_a, gm_a, 1)),
                {},
                node_a_copy_name,
            )
            return node_a_copy

    else:
        raise AssertionError(
            f"handling of node {node_a.format_node()} with op {node_a.op} is not implemented"
        )

