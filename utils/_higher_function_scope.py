
def _higher_function_scope(node: nodes.NodeNG) -> nodes.FunctionDef | None:
    """Search for the first function which encloses the given
    scope.

    This can be used for looking up in that function's
    scope, in case looking up in a lower scope for a particular
    name fails.

    :param node: A scope node.
    :returns:
        ``None``, if no parent function scope was found,
        otherwise an instance of :class:`astroid.nodes.scoped_nodes.Function`,
        which encloses the given node.
    """
    current = node
    while current.parent and not isinstance(current.parent, nodes.FunctionDef):
        current = current.parent
    if current and current.parent:
        return current.parent
    return None

