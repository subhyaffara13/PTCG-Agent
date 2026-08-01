
def get_extra_size_of(node: Node, nodes: set[Node]) -> int:
    """Given a node and a set of nodes,
    this function return the extra size that needed
    if this node is included in this set.
    """
    # Find all its input nodes
    input_nodes: dict[Node, None] = {}
    map_arg(node.args, input_nodes.setdefault)
    map_arg(node.kwargs, input_nodes.setdefault)
    # Calculate total size of related nodes
    total_size_of_input_nodes = 0
    for n in input_nodes:
        # Make sure this node hasn't been in this set yet
        if n not in nodes:
            size_bytes = getattr(n, "size_bytes", None)
            if size_bytes:
                total_size_of_input_nodes += size_bytes.output_size
            else:
                raise RuntimeError("node has no size_bytes attr")
    # Don't forget the op node itself
    size_bytes = getattr(node, "size_bytes", None)
    if size_bytes:
        total_size_of_input_nodes += size_bytes.total_size
    else:
        raise RuntimeError("node has no size_bytes attr")
    return total_size_of_input_nodes

