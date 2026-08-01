
def is_expr_literal_type(node: Expression) -> bool:
    """Returns 'true' if the given node is a Literal"""
    if isinstance(node, IndexExpr):
        base = node.base
        return isinstance(base, RefExpr) and base.fullname in LITERAL_TYPE_NAMES
    if isinstance(node, NameExpr):
        underlying = node.node
        return isinstance(underlying, TypeAlias) and isinstance(
            get_proper_type(underlying.target), LiteralType
        )
    return False

