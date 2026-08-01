
def insert_weight_and_bias_get_attr_node_from_get_attr_to_qtensor(
    gm: torch.fx.GraphModule,
    get_attr_to_weight_node: torch.fx.Node,
    get_attr_to_bias_node: torch.fx.Node | None,
) -> tuple[torch.fx.Node, torch.fx.Node | None]:
    if not isinstance(get_attr_to_weight_node.target, str):
        raise AssertionError(
            f"expected str target, got {type(get_attr_to_weight_node.target).__name__}"
        )
    w_qtensor = getattr(gm, get_attr_to_weight_node.target)
    w_attr_name = f"dequantized_{get_attr_to_weight_node.target}_w"

    if get_attr_to_bias_node is not None:
        if not isinstance(get_attr_to_bias_node.target, str):
            raise AssertionError(
                f"expected str target, got {type(get_attr_to_bias_node.target).__name__}"
            )
        b_qtensor = getattr(gm, get_attr_to_bias_node.target)
        b_attr_name = f"dequantized_{get_attr_to_bias_node.target}_b"
    else:
        b_qtensor, b_attr_name = None, ""

    return insert_weight_and_bias_get_attr_node(
        gm, w_qtensor, b_qtensor, w_attr_name, b_attr_name
    )

