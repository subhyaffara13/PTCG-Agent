
def literal(e: Expression) -> int:
    """Return the literal kind for an expression."""

    if isinstance(e, ComparisonExpr):
        return min(literal(o) for o in e.operands)

    elif isinstance(e, OpExpr):
        return min(literal(e.left), literal(e.right))

    elif isinstance(e, (MemberExpr, UnaryExpr, StarExpr)):
        return literal(e.expr)

    elif isinstance(e, AssignmentExpr):
        return literal(e.target)

    elif isinstance(e, IndexExpr):
        if literal(e.index) == LITERAL_YES:
            return literal(e.base)
        else:
            return LITERAL_NO

    elif isinstance(e, NameExpr):
        if isinstance(e.node, Var) and e.node.is_final and e.node.final_value is not None:
            return LITERAL_YES
        return LITERAL_TYPE

    if isinstance(e, (IntExpr, FloatExpr, ComplexExpr, StrExpr, BytesExpr)):
        return LITERAL_YES

    if literal_hash(e):
        return LITERAL_YES

    return LITERAL_NO

