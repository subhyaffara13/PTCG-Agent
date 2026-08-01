
def returns_something(return_node: nodes.Return) -> bool:
    """Check if a return node returns a value other than None.

    :param return_node: The return node to check.
    :type return_node: nodes.Return

    :rtype: bool
    :return: True if the return node returns a value other than None,
        False otherwise.
    """
    returns = return_node.value
    return not (
        returns is None or (isinstance(returns, nodes.Const) and returns.value is None)
    )

