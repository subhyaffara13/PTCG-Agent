
def get_contextlib_with_statements(node: nodes.NodeNG) -> Iterator[nodes.With]:
    """Get all contextlib.with statements in the ancestors of the given node."""
    for with_node in node.node_ancestors():
        if isinstance(with_node, nodes.With):
            yield with_node

