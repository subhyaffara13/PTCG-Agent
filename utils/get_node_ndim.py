
def get_node_ndim(nodes: Sequence[Node]) -> dict[Node, int]:
    """
    Returns a dict map a node to 'ndim'.
    """
    node_ndim = {}
    for node in nodes:
        ft = get_fake_tensor_from_node_arg(node)
        assert ft is not None
        node_ndim[node] = ft.ndim
    return node_ndim

