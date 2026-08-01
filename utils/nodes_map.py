
def nodes_map(nodes: list[torch.fx.Node], node_call_back) -> list[torch.fx.Node]:
    """
    Sequentially visit the nodes list and invoke node_call_back on each element.
    Returns the nodes list after the node_call_back is invoked on each element.
    """
    for node in nodes:
        node_call_back(node)
    return nodes

