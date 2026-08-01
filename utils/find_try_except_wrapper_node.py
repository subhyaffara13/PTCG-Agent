
def find_try_except_wrapper_node(
    node: nodes.NodeNG,
) -> nodes.ExceptHandler | nodes.Try | None:
    """Return the ExceptHandler or the Try node in which the node is."""
    current = node
    ignores = (nodes.ExceptHandler, nodes.Try)
    while current and not isinstance(current.parent, ignores):
        current = current.parent

    if current and isinstance(current.parent, ignores):
        return current.parent
    return None

