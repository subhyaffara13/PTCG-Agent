
def get_setters_property(node: nodes.FunctionDef) -> nodes.FunctionDef | None:
    """Get the property node for the given setter node.

    :param node: The node to get the property for.
    :type node: nodes.FunctionDef

    :rtype: nodes.FunctionDef or None
    :returns: The node relating to the property of the given setter node,
        or None if one could not be found.
    """
    property_ = None

    property_name = get_setters_property_name(node)
    class_node = utils.node_frame_class(node)
    if property_name and class_node:
        class_attrs: list[nodes.FunctionDef] = class_node.getattr(node.name)
        for attr in class_attrs:
            if utils.decorated_with_property(attr):
                property_ = attr
                break

    return property_

