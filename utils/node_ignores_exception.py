
def node_ignores_exception(
    node: nodes.NodeNG, exception: type[Exception] | str = Exception
) -> bool:
    """Check if the node is in a Try which handles the given exception.

    If the exception is not given, the function is going to look for bare
    excepts.
    """
    managing_handlers = get_exception_handlers(node, exception)
    if managing_handlers:
        return True
    return any(get_contextlib_suppressors(node, exception))

