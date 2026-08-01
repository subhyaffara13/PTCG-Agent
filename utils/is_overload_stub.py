
def is_overload_stub(node: nodes.NodeNG) -> bool:
    """Check if a node is a function stub decorated with typing.overload.

    :param node: Node to check.
    :returns: True if node is an overload function stub. False otherwise.
    """
    decorators = getattr(node, "decorators", None)
    return bool(decorators and decorated_with(node, ["typing.overload", "overload"]))

