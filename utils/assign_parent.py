
def assign_parent(node: nodes.NodeNG) -> nodes.NodeNG:
    """Return the higher parent which is not an AssignName, Tuple or List node."""
    while node and isinstance(node, (nodes.AssignName, nodes.Tuple, nodes.List)):
        node = node.parent
    return node

