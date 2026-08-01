
def is_node_inside_try_except(node: nodes.Raise) -> bool:
    """Check if the node is directly under a Try/Except statement
    (but not under an ExceptHandler!).

    Args:
        node (nodes.Raise): the node raising the exception.

    Returns:
        bool: True if the node is inside a try/except statement, False otherwise.
    """
    context = find_try_except_wrapper_node(node)
    return isinstance(context, nodes.Try)

