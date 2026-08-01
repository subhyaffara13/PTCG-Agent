
def _looks_like_type_subscript(node: nodes.Name) -> bool:
    """
    Try to figure out if a Name node is used inside a type related subscript.

    :param node: node to check
    :type node: astroid.nodes.NodeNG
    :return: whether the node is a Name node inside a type related subscript
    """
    if isinstance(node.parent, nodes.Subscript):
        return node.name == "type"
    return False

