
def _looks_like_typing_alias(node: nodes.Call) -> bool:
    """
    Returns True if the node corresponds to a call to _alias function.

    For example :

    MutableSet = _alias(collections.abc.MutableSet, T)

    :param node: call node
    """
    return (
        isinstance(node.func, nodes.Name)
        # TODO: remove _DeprecatedGenericAlias when Py3.14 min
        and node.func.name in {"_alias", "_DeprecatedGenericAlias"}
        and len(node.args) == 2
        and (
            # _alias function works also for builtins object such as list and dict
            isinstance(node.args[0], (nodes.Attribute, nodes.Name))
        )
    )

