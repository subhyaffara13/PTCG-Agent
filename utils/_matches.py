
def _matches(node1: nodes.NodeNG | bases.Proxy, node2: nodes.NodeNG) -> bool:
    """Returns True if the two nodes match."""
    if isinstance(node1, nodes.Name) and isinstance(node2, nodes.Name):
        return node1.name == node2.name
    if isinstance(node1, nodes.Attribute) and isinstance(node2, nodes.Attribute):
        return node1.attrname == node2.attrname and _matches(node1.expr, node2.expr)
    if isinstance(node1, nodes.Const) and isinstance(node2, nodes.Const):
        return node1.value == node2.value

    return False

