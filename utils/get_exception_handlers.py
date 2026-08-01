
def get_exception_handlers(
    node: nodes.NodeNG, exception: type[Exception] | str = Exception
) -> list[nodes.ExceptHandler] | None:
    """Return the collections of handlers handling the exception in arguments.

    Args:
        node (nodes.NodeNG): A node that is potentially wrapped in a try except.
        exception (builtin.Exception or str): exception or name of the exception.

    Returns:
        list: the collection of handlers that are handling the exception or None.
    """
    context = find_try_except_wrapper_node(node)
    if isinstance(context, nodes.Try):
        return [
            handler for handler in context.handlers if error_of_type(handler, exception)
        ]
    return []

