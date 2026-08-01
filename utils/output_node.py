
def output_node(gm: torch.fx.GraphModule) -> Node:
    """Get the output node from an FX graph"""
    last_node = next(iter(reversed(gm.graph.nodes)))
    assert last_node.op == "output"
    return last_node

