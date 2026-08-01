
def refers_to_fullname(node: Expression, fullnames: str | tuple[str, ...]) -> bool:
    """Is node a name or member expression with the given full name?"""
    if not isinstance(fullnames, tuple):
        fullnames = (fullnames,)

    if not isinstance(node, RefExpr):
        return False
    if node.fullname in fullnames:
        return True
    if isinstance(node.node, TypeAlias) and not node.node.python_3_12_type_alias:
        return is_named_instance(node.node.target, fullnames)
    return False

