
def is_being_called(node: nodes.NodeNG) -> bool:
    """Return True if node is the function being called in a Call node."""
    return isinstance(node.parent, nodes.Call) and node.parent.func is node

