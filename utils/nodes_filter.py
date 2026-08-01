
def nodes_filter(nodes: list[torch.fx.Node], node_call_back) -> list[torch.fx.Node]:
    """Returns the nodes that match the node_call_back as a list."""
    return [node for node in nodes if node_call_back(node)]

