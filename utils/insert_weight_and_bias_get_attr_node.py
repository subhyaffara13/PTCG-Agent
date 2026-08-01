
def insert_weight_and_bias_get_attr_node(
    gm: torch.fx.GraphModule,
    w_qtensor: torch.Tensor,
    b_qtensor: torch.Tensor | None,
    w_attr_name: str,
    b_attr_name: str,
) -> tuple[torch.fx.Node, torch.fx.Node | None]:
    w_tensor = get_tensor_from_qtensor(w_qtensor)
    _assign_attr(w_tensor, gm, w_attr_name)
    w_tensor_attr = gm.graph.get_attr(w_attr_name)

    if b_qtensor is not None:
        b_tensor = get_tensor_from_qtensor(b_qtensor, dequant=False)
        _assign_attr(b_tensor, gm, b_attr_name)
        b_tensor_attr = gm.graph.get_attr(b_attr_name)
    else:
        b_tensor_attr = None

    return w_tensor_attr, b_tensor_attr

