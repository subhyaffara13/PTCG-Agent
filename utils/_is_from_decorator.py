
def _is_from_decorator(node) -> bool:
    """Return whether the given node is the child of a decorator."""
    return any(isinstance(parent, nodes.Decorators) for parent in node.node_ancestors())

