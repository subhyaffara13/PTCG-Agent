
def get_node_is_scalar(nodes: Sequence[Node]) -> dict[Node, bool]:
    """
    Returns a dict map a node to 'is_scalar'.
    """
    node_is_scalar = {}
    for node in nodes:
        ft = get_fake_tensor_from_node_arg(node)
        assert ft is not None
        node_is_scalar[node] = ft.numel() == 1
    return node_is_scalar

