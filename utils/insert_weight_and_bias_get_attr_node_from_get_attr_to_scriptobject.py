
def insert_weight_and_bias_get_attr_node_from_get_attr_to_scriptobject(
    gm: torch.fx.GraphModule,
    param_node: torch.fx.Node,
) -> tuple[torch.fx.Node, torch.fx.Node | None]:
    """Directly inline tensor from a get_attr fx node."""
    mod = get_script_object(gm, param_node)
    w_qtensor, b_qtensor = mod.unpack()  # type: ignore[attr-defined]
    w_attr_name, b_attr_name = (
        f"dequantized_{param_node.target}_w",
        f"dequantized_{param_node.target}_b",
    )
    return insert_weight_and_bias_get_attr_node(
        gm, w_qtensor, b_qtensor, w_attr_name, b_attr_name
    )

