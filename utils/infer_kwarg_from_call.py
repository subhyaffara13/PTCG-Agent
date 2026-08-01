
def infer_kwarg_from_call(call_node: nodes.Call, keyword: str) -> nodes.Name | None:
    """Returns the specified argument from a function's kwargs.

    :param nodes.Call call_node: Node representing a function call to check.
    :param str keyword: Name of the argument to be extracted.

    :returns: The node representing the argument, None if the argument is not found.
    :rtype: nodes.Name
    """
    for arg in call_node.kwargs:
        inferred = safe_infer(arg.value)
        if isinstance(inferred, nodes.Dict):
            for item in inferred.items:
                if item[0].value == keyword:
                    return item[1]

    return None

