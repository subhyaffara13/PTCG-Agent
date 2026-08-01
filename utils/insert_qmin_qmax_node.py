
def insert_qmin_qmax_node(
    gm: torch.fx.GraphModule, dtype_node: torch.dtype | torch.fx.Node
) -> tuple[torch.fx.Node, torch.fx.Node]:
    q_min_max_node = gm.graph.call_function(
        calculate_qmin_qmax, (None, None, False, dtype_node, False)
    )
    qmin_node = gm.graph.call_function(operator.getitem, (q_min_max_node, 0))
    qmax_node = gm.graph.call_function(operator.getitem, (q_min_max_node, 1))
    return qmin_node, qmax_node

