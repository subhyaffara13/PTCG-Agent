
def _looks_like_functools_member(
    node: nodes.Attribute | nodes.Call, member: str
) -> bool:
    """Check if the given Call node is the wanted member of functools."""
    if isinstance(node, nodes.Attribute):
        return node.attrname == member
    if isinstance(node.func, nodes.Name):
        return node.func.name == member
    if isinstance(node.func, nodes.Attribute):
        return (
            node.func.attrname == member
            and isinstance(node.func.expr, nodes.Name)
            and node.func.expr.name == "functools"
        )
    return False

