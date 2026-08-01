
def has_higher_order_op(gm: fx.GraphModule) -> bool:
    # Check if there is a higher order op in the graph
    for node in gm.graph.nodes:
        if node.op == "get_attr":
            maybe_param = getattr(gm, node.target)
            if isinstance(maybe_param, torch.fx.GraphModule):
                return True
    return False

