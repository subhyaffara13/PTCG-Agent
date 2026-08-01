
def ignore_node(node: Expression) -> bool:
    """Return True if node is to be omitted from test case output."""

    # We want to get rid of object() expressions in the typing module stub
    # and also TypeVar(...) expressions. Since detecting whether a node comes
    # from the typing module is not easy, we just to strip them all away.
    if isinstance(node, TypeVarExpr):
        return True
    if isinstance(node, NameExpr) and node.fullname == "builtins.object":
        return True
    if isinstance(node, NameExpr) and node.fullname == "builtins.None":
        return True
    if isinstance(node, CallExpr) and (ignore_node(node.callee) or node.analyzed):
        return True

    return False

