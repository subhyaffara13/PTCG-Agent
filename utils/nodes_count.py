
def nodes_count(nodes: list[torch.fx.Node], node_call_back) -> int:
    """Returns the number of nodes that match the node_call_back."""
    return len(nodes_filter(nodes, node_call_back))

