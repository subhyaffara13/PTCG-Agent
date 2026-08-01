
def get_setters_property_name(node: nodes.FunctionDef) -> str | None:
    """Get the name of the property that the given node is a setter for.

    :param node: The node to get the property name for.
    :type node: str

    :rtype: str or None
    :returns: The name of the property that the node is a setter for,
        or None if one could not be found.
    """
    decorators = node.decorators.nodes if node.decorators else []
    for decorator in decorators:
        match decorator:
            case nodes.Attribute(attrname="setter", expr=nodes.Name(name=name)):
                return name  # type: ignore[no-any-return]
    return None

